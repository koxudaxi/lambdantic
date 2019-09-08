# lambdantic
[Pydantic](https://github.com/samuelcolvin/pydantic) model and lambda event handler for [AWS Lambda](https://aws.amazon.com/lambda/)

[![Build Status](https://travis-ci.org/koxudaxi/lambdantic.svg?branch=master)](https://travis-ci.org/koxudaxi/lambdantic)
[![PyPI version](https://badge.fury.io/py/lambdantic.svg)](https://badge.fury.io/py/lambdantic)
[![codecov](https://codecov.io/gh/koxudaxi/lambdantic/branch/master/graph/badge.svg)](https://codecov.io/gh/koxudaxi/lambdantic)


## This project is an experimental phase.

## What is Lambdantic ?
The name means [AWS Lambda](https://aws.amazon.com/lambda/) + [pydantic](https://github.com/samuelcolvin/pydantic)

`lambdantic` dispatch handler function from aws lambda events and to assign attributes from event object.

## Installation

To install `lambdantic`:
```sh
$ pip install lambdantic
```

## Example
### API Gateway
The example is simple api which is invoked by API Gateway.

`lambdantic` parse  [Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html) request.

The example should be deployed by [Serverless](https://serverless.com/), [AWS CDK](https://github.com/aws/aws-cdk) or other framework which supports [Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html).

```python
# handler.py
from typing import List, Optional

from pydantic import BaseModel, Schema

from lambdantic.apigateway import Handler

handler = Handler()


class Pet(BaseModel):
    pet_id: Optional[int] = Schema(..., alias='id')
    name: str
    age: int


# database
pets = [
        Pet(id=1, name='dog', age=3),
        Pet(id=2, name='cat', age=2)
    ]


@handler.get('/pets')
def get_pets() -> List[Pet]:
    return pets


@handler.get('/pets/<pet_id>')
def get_pet(pet_id: int) -> Pet:
    for pet in pets:
        if pet.pet_id == pet_id:
            return pet


@handler.post('/pets', body_model=Pet, status_code=201)
def crate_pet(pet: Pet) -> Pet:
    pet.pet_id = max(p.pet_id for p in pets)
    pets.append(pet)

    return pet
```

If you use Serverless then, the handler is defined like this example.
```yaml
functions:
  pet:
    handler: handler.handler
    events:
      - http:
          method: any
          path: /{proxy+}
```

I show common parameters for Other framework 
```
Handler: handler.handler
API Gateway API integration type : Lambda Proxy Integration
Path: /{proxy+}
method: ANY
```

## Implemented
- API Gateway (WIP)

## Not Implemented
- S3
- SNS
... and more


## Development

Install the package in editable mode:

```sh
$ git clone git@github.com:koxudaxi/lambdantic.git
$ pip install -e lambdantic
```

## PyPi 

[https://pypi.org/project/lambdantic](https://pypi.org/project/lambdantic)

## Source Code

[https://github.com/koxudaxi/lambdantic](https://github.com/koxudaxi/lambdantic)

## Documentation

[https://koxudaxi.github.io/lambdantic](https://koxudaxi.github.io/lambdantic)

## License

lambdantic is released under the MIT License. http://www.opensource.org/licenses/mit-license
