
resource "aws_lambda_function" "base_lambda" {
  filename          = "base.zip"
  function_name     = "base"
  role              = "arn:aws:iam::253712699852:role/lambda_basic_execution"
  handler           = "base.lambda_handler"
  runtime           = "python3.6"
  source_code_hash = "${base64sha256(file("base.zip"))}"

  /*environment {
    variables = {
      huh = "dawe"
    }
  }*/
}

resource "aws_lambda_function" "connector_lambda" {
  filename          = "connector.zip"
  function_name     = "connector"
  role              = "arn:aws:iam::253712699852:role/lambda_basic_execution"
  handler           = "connector.lambda_handler"
  runtime           = "python3.6"
  source_code_hash  = "${base64sha256(file("connector.zip"))}"

  /*environment {
    variables = {
      huh = "dawe"
    }
  }*/
}

resource "aws_sns_topic_subscription" "base_to_connector"{
  topic_arn         = "arn:aws:sns:us-east-1:253712699852:iot_topic"
  protocol          = "lambda"
  endpoint          = "arn:aws:lambda:us-east-1:253712699852:function:connector"
}
