from __future__ import annotations

import json
import re
from collections import OrderedDict, defaultdict
from functools import wraps
from http import HTTPStatus
from inspect import _empty as empty, signature  # type: ignore
from logging import getLogger
from typing import Any, Callable, Dict, List, Optional, Type

from lambdantic import dump_obj
from pydantic import BaseModel, ValidationError
from pydantic.fields import Shape

from ..fields import Field, FieldType
from .exceptions import LambdaError
from .models import HttpMethod, Request, Response

logger = getLogger(__name__)


class Handler:
    def __init__(self) -> None:
        self.routes: Dict[HttpMethod, OrderedDict[str, Callable]] = defaultdict(
            OrderedDict
        )

    def __call__(
        self, event: Dict[str, Any], context: Any, *args: Any, **kwargs: Any
    ) -> Dict[str, Any]:
        path: str = event['path']
        method: str = event['httpMethod']

        for path_pattern, func in self.routes[HttpMethod(method)].items():
            matched = re.search(path_pattern, path)
            if matched:
                func = self.routes[HttpMethod(method)][path_pattern]
                response: Response = func(
                    event=event, context=context, path_parameters=matched.groupdict()
                )
                return response.dict()
        return Response(statusCode=HTTPStatus.NOT_FOUND).dict()

    def set_route(self, method: HttpMethod, path_pattern: str, func: Callable) -> None:
        self.routes[method][path_pattern] = func
        self.routes[method] = OrderedDict(
            sorted(  # type: ignore
                self.routes[method].items(),
                key=lambda item: item[0].count('/'),
                reverse=True,
            )
        )

    def get(
        self,
        path: str,
        *,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:
        return self.route(
            path,
            method=HttpMethod.GET,
            path_parameter_model=path_parameter_model,
            query_parameter_model=query_parameter_model,
            multi_value_query_parameter_model=multi_value_query_parameter_model,
            body_model=body_model,
            response_model_skip_defaults=response_model_skip_defaults,
            status_code=status_code,
            pass_event=pass_event,
            pass_context=pass_context,
        )

    def head(
        self,
        path: str,
        *,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:
        return self.route(
            path,
            method=HttpMethod.HEAD,
            path_parameter_model=path_parameter_model,
            query_parameter_model=query_parameter_model,
            multi_value_query_parameter_model=multi_value_query_parameter_model,
            body_model=body_model,
            response_model_skip_defaults=response_model_skip_defaults,
            status_code=status_code,
            pass_event=pass_event,
            pass_context=pass_context,
        )

    def delete(
        self,
        path: str,
        *,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:
        return self.route(
            path,
            method=HttpMethod.DELETE,
            path_parameter_model=path_parameter_model,
            query_parameter_model=query_parameter_model,
            multi_value_query_parameter_model=multi_value_query_parameter_model,
            body_model=body_model,
            response_model_skip_defaults=response_model_skip_defaults,
            status_code=status_code,
            pass_event=pass_event,
            pass_context=pass_context,
        )

    def option(
        self,
        path: str,
        *,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:
        return self.route(
            path,
            method=HttpMethod.OPTION,
            path_parameter_model=path_parameter_model,
            query_parameter_model=query_parameter_model,
            multi_value_query_parameter_model=multi_value_query_parameter_model,
            body_model=body_model,
            response_model_skip_defaults=response_model_skip_defaults,
            status_code=status_code,
            pass_event=pass_event,
            pass_context=pass_context,
        )

    def patch(
        self,
        path: str,
        *,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:
        return self.route(
            path,
            method=HttpMethod.PATCH,
            path_parameter_model=path_parameter_model,
            query_parameter_model=query_parameter_model,
            multi_value_query_parameter_model=multi_value_query_parameter_model,
            body_model=body_model,
            response_model_skip_defaults=response_model_skip_defaults,
            status_code=status_code,
            pass_event=pass_event,
            pass_context=pass_context,
        )

    def post(
        self,
        path: str,
        *,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:
        return self.route(
            path,
            method=HttpMethod.POST,
            path_parameter_model=path_parameter_model,
            query_parameter_model=query_parameter_model,
            multi_value_query_parameter_model=multi_value_query_parameter_model,
            body_model=body_model,
            response_model_skip_defaults=response_model_skip_defaults,
            status_code=status_code,
            pass_event=pass_event,
            pass_context=pass_context,
        )

    def put(
        self,
        path: str,
        *,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:
        return self.route(
            path,
            method=HttpMethod.PUT,
            path_parameter_model=path_parameter_model,
            query_parameter_model=query_parameter_model,
            multi_value_query_parameter_model=multi_value_query_parameter_model,
            body_model=body_model,
            response_model_skip_defaults=response_model_skip_defaults,
            status_code=status_code,
            pass_event=pass_event,
            pass_context=pass_context,
        )

    def route(
        self,
        path: str,
        *,
        method: HttpMethod = HttpMethod.GET,
        path_parameter_model: Optional[Type[BaseModel]] = None,
        query_parameter_model: Optional[Type[BaseModel]] = None,
        multi_value_query_parameter_model: Optional[Type[BaseModel]] = None,
        body_model: Optional[Type[BaseModel]] = None,
        response_model_skip_defaults: bool = False,
        status_code: HTTPStatus = HTTPStatus.OK,
        pass_event: bool = False,
        pass_context: bool = False,
    ) -> Callable:

        path_pattern, path_parameter_count = re.subn(
            r'<([^/>]+)>', r'(?P\g<0>[^/]+)', path
        )

        event_context_argument_count = sum([pass_event, pass_context])
        expected_argument_count = (
            sum(
                model_class is not None
                for model_class in (
                    query_parameter_model,
                    multi_value_query_parameter_model,
                    body_model,
                )
            )
            + path_parameter_count
            if path_parameter_model is None
            else 1 + event_context_argument_count
        )

        def inner(func: Callable) -> Callable[[Any], Response]:
            sig = signature(func)
            parameters = sig.parameters
            if 'self' in parameters and list(sig.parameters)[0] == 'self':
                self_count = 1
            else:
                self_count = 0
            if len(parameters) != expected_argument_count:
                raise Exception(
                    f'signature does not invalid. function:{func} parameters:{sig.parameters}'
                )

            base_parameter_count = self_count + event_context_argument_count
            fields: Dict[str, Optional[Field]] = {}
            start_pos = base_parameter_count
            end_pos = path_parameter_count + base_parameter_count
            for name, path_parameter in list(sig.parameters.items())[start_pos:end_pos]:
                if path_parameter.annotation == empty:
                    fields[name] = None
                else:
                    fields[name] = FieldType.path_parameter.get_field(
                        path_parameter.annotation, name=name
                    )
            if sig.return_annotation != empty:
                response_field: Optional[Field] = FieldType.response.get_field(
                    sig.return_annotation
                )
            else:
                response_field = None

            @wraps(func)
            def receive_params(
                *args: Any,
                event: Dict[str, Any],
                context: Any,
                path_parameters: Dict[str, Any],
            ) -> Response:
                try:
                    request = Request.parse_obj(event)
                    arguments: List = list(args)  # self
                    if pass_event:
                        arguments.append(event)
                    if pass_context:
                        arguments.append(context)
                    if path_parameter_model:
                        arguments.append(
                            path_parameter_model.parse_obj(path_parameters)
                        )
                    else:
                        for (
                            path_parameter_name,
                            path_parameter_value,
                        ) in path_parameters.items():
                            field = fields[path_parameter_name]
                            if field:
                                result, error = field.validate(path_parameter_value)
                                arguments.append(result)
                                if error:
                                    logger.warning(
                                        f'Validation Error: path_parameter is invalid'
                                        f' name:{path_parameter_name}, value: {path_parameter_value}'
                                    )
                                    return Response(statusCode=HTTPStatus.BAD_REQUEST)
                            else:
                                arguments.append(path_parameter_value)
                    if query_parameter_model:
                        arguments.append(
                            query_parameter_model.parse_obj(
                                request.queryStringParameters
                            )
                        )
                    if multi_value_query_parameter_model:
                        arguments.append(
                            multi_value_query_parameter_model.parse_obj(
                                request.multiValueQueryStringParameters
                            )
                        )
                    if body_model:
                        try:
                            arguments.append(
                                body_model.parse_raw(request.decoded_body or '{}')
                            )
                        except ValidationError as e:
                            logger.warning(e)
                            return Response(statusCode=HTTPStatus.BAD_REQUEST)
                    response: Any = func(*arguments)

                    if response_field is None:
                        if response is None:
                            return Response(statusCode=status_code)
                        else:
                            return Response(statusCode=HTTPStatus.BAD_REQUEST)

                    response, error = response_field.validate(response)

                    if error:
                        logger.warning(str(error))
                        return Response(statusCode=HTTPStatus.BAD_REQUEST)
                    if isinstance(response, Response):
                        return response

                    json_data = json.dumps(
                        dump_obj(response, skip_defaults=response_model_skip_defaults)
                    )
                    return Response(
                        body=json_data, statusCode=status_code
                    )  # type: ignore

                except LambdaError as e:
                    return e.response
                except Exception as e:
                    logger.error(str(e))
                    return Response(statusCode=HTTPStatus.INTERNAL_SERVER_ERROR)

            self.set_route(method, path_pattern, receive_params)

            return receive_params

        return inner
