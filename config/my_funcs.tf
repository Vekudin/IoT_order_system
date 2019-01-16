
resource "aws_lambda_function" "order_handler_lambda" {
  filename          = "order_handler.zip"
  function_name     = "order_handler"
  role              = "arn:aws:iam::253712699852:role/lambda_basic_execution"
  handler           = "order_handler.lambda_handler"
  runtime           = "python3.6"
  source_code_hash  = "${base64sha256(file("order_handler.zip"))}"
}

resource "aws_lambda_function" "car_caller_lambda" {
  filename          = "car_caller.zip"
  function_name     = "car_caller"
  role              = "arn:aws:iam::253712699852:role/lambda_basic_execution"
  handler           = "car_caller.lambda_handler"
  runtime           = "python3.6"
  source_code_hash  = "${base64sha256(file("car_caller.zip"))}"
}

resource "aws_sns_topic_subscription" "sns_to_iot_subscriptin"{
  topic_arn         = "arn:aws:sns:us-east-1:253712699852:orders_topic"
  protocol          = "lambda"
  endpoint          = "${aws_lambda_function.car_caller_lambda.arn}"
}
