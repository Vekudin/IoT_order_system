
resource "aws_iot_topic_rule" "sns_iot" {
  name              = "sns_iot"
  description       = "Rule that connects SNS topic with IOT"
  enabled           = true
  sql               = "SELECT * FROM 'aliens/messages'"
  sql_version       = "2015-10-08"

  lambda {
    function_arn    = "${aws_lambda_function.base_lambda.arn}"
  }
}
