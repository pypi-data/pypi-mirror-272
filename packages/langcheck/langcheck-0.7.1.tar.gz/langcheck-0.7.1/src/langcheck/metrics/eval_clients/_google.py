import google.generativeai as genai

from ._base import EvalClient


class OpenAIEvalClient(EvalClient):
    '''EvalClient defined for OpenAI API.
    '''

    def __init__(self,
                 openai_client: OpenAI | None = None,
                 openai_args: dict[str, str] | None = None,
                 *,
                 use_async: bool = False):
        '''
        Intialize the OpenAI evaluation client.

        Args:
            openai_client: (Optional) The OpenAI client to use.
            openai_args: (Optional) dict of additional args to pass in to the
            ``client.chat.completions.create`` function
            use_async: (Optional) If True, the async client will be used.
        '''
        if openai_client:
            self._client = openai_client
        elif use_async:
            self._client = AsyncOpenAI()
        else:
            self._client = OpenAI()

        self._openai_args = openai_args
        self._use_async = use_async

    def _call_api(self,
                  prompts: Iterable[str | None],
                  config: dict[str, str],
                  *,
                  tqdm_description: str | None = None) -> list[Any]:
        # A helper function to call the API with exception filter for alignment
        # of exception handling with the async version.
        def _call_api_with_exception_filter(model_input: dict[str, Any]) -> Any:
            if model_input is None:
                return None
            try:
                return self._client.chat.completions.create(**model_input)
            except Exception as e:
                return e

        model_inputs = [{
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            **config
        } for prompt in prompts]

        if self._use_async:
            # A helper function to call the async API.
            async def _call_async_api() -> list[Any]:
                responses = await asyncio.gather(*map(
                    lambda model_input: self._client.chat.completions.create(
                        **model_input), model_inputs),
                                                 return_exceptions=True)
                return responses

            responses = asyncio.run(_call_async_api())
        else:
            responses = [
                _call_api_with_exception_filter(model_input)
                for model_input in tqdm_wrapper(model_inputs,
                                                desc=tqdm_description)
            ]

        # Filter out exceptions and print them out.
        for i, response in enumerate(responses):
            if not isinstance(response, Exception):
                continue
            print('OpenAI failed to return an assessment corresponding to '
                  f'{i}th prompt: {response}')
            responses[i] = None
        return responses

    def get_text_responses(
            self,
            prompts: Iterable[str],
            *,
            tqdm_description: str | None = None) -> list[str | None]:
        '''The function that gets resonses to the given prompt texts.
        We use OpenAI's 'gpt-turbo-3.5' model by default, but you can configure
        it by passing the 'model' parameter in the openai_args.

        Args:
            prompts: The prompts you want to get the responses for.

        Returns:
            A list of responses to the prompts. The responses can be None if the
            evaluation fails.
        '''
        config = {"model": "gpt-3.5-turbo", "seed": 123}
        config.update(self._openai_args or {})
        tqdm_description = tqdm_description or 'Intermediate assessments (1/2)'  # NOQA: E501
        responses = self._call_api(prompts=prompts,
                                   config=config,
                                   tqdm_description=tqdm_description)
        response_texts = [
            response.choices[0].message.content if response else None
            for response in responses
        ]

        return response_texts

    def get_float_score(
            self,
            metric_name: str,
            language: str,
            unstructured_assessment_result: list[str | None],
            score_map: dict[str, float],
            *,
            tqdm_description: str | None = None) -> list[float | None]:
        '''The function that transforms the unstructured assessments (i.e. long
        texts that describe the evaluation results) into scores. We leverage the
        function calling API to extract the short assessment results from the
        unstructured assessments, so please make sure that the model you use
        supports function calling
        (https://platform.openai.com/docs/guides/gpt/function-calling).

        Ref:
            https://platform.openai.com/docs/guides/gpt/function-calling

        Args:
            metric_name: The name of the metric to be used. (e.g. "toxicity")
            language: The language of the prompts. (e.g. "en")
            unstructured_assessment_result: The unstructured assessment results
                for the given assessment prompts.
            score_map: The mapping from the short assessment results
                (e.g. "Good") to the scores.
            tqdm_description: The description to be shown in the tqdm bar.

        Returns:
            A list of scores for the given prompts. The scores can be None if
            the evaluation fails.
        '''
        if language not in ['en', 'ja', 'de', 'zh']:
            raise ValueError(f'Unsupported language: {language}')

        fn_call_template = get_template(f'{language}/get_score/openai.j2')

        options = list(score_map.keys())
        fn_call_messages = [
            fn_call_template.render({
                'metric': metric_name,
                'unstructured_assessment': unstructured_assessment,
                'options': options,
            }) if unstructured_assessment else None
            for unstructured_assessment in unstructured_assessment_result
        ]

        functions = [{
            'name': 'save_assessment',
            'description': f'Save the assessment of {metric_name}.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'assessment': {
                        'type': 'string',
                        'enum': options,
                        'description': f'The assessment of {metric_name}.',
                    },
                },
                'required': ['assessment'],
            },
        }]

        config_structured_assessments = {
            "seed": 123,
            "functions": functions,
            "function_call": {
                "name": 'save_assessment',
            },
            "model": "gpt-3.5-turbo"
        }
        config_structured_assessments.update(self._openai_args or {})

        tqdm_description = tqdm_description or 'Scores (2/2)'
        responses = self._call_api(prompts=fn_call_messages,
                                   config=config_structured_assessments,
                                   tqdm_description=tqdm_description)
        function_args = [
            json.loads(response.choices[0].message.function_call.arguments)
            if response else None for response in responses
        ]
        assessments = [
            function_arg.get('assessment') if function_arg else None
            for function_arg in function_args
        ]

        # Check if any of the assessments are not recognized.
        for assessment in assessments:
            if (assessment is None) or (assessment in options):
                continue
            # By leveraging the function calling API, this should be pretty
            # rare, but we're dealing with LLMs here so nothing is absolute!
            print(f'OpenAI returned an unrecognized assessment: "{assessment}"')

        return [
            score_map[assessment] if assessment else None
            for assessment in assessments
        ]

    def similarity_scorer(self) -> OpenAISimilarityScorer:
        '''
        https://openai.com/blog/new-embedding-models-and-api-updates
        '''
        assert isinstance(
            self._client,
            OpenAI), "Only sync clients are supported for similarity scoring."
        return OpenAISimilarityScorer(openai_client=self._client,
                                      openai_args=self._openai_args)
