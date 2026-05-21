# AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Copy all source files into the Lambda task root
COPY sourcec/ ${LAMBDA_TASK_ROOT}/

# Lambda handler: file=lambda_handler, function=handler
CMD ["lambda_handler.handler"]