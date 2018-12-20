//resource "aws_iam_role" "iam_for_lambda" {
//  name = "iam_for_lambda"
//
//  assume_role_policy = <<EOF
//{
//  "Version": "2012-10-17",
//  "Statement": [
//    {
//      "Action": "sts:AssumeRole",
//      "Principal": {
//        "Service": "lambda.amazonaws.com"
//      },
//      "Effect": "Allow",
//      "Sid": ""
//    }
//  ]
//}
//EOF
//}

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
  source_code_hash = "${base64sha256(file("connector.zip"))}"

  /*environment {
    variables = {
      huh = "dawe"
    }
  }*/
}
