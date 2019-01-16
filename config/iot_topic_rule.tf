
resource "aws_iot_topic_rule" "iot_to_order_handler_rule" {
  name              = "iot_to_order_handler"
  description       = "Rule that manages IoT data by transporting it to the orders lambda function"
  enabled           = true
  sql               = "SELECT * FROM 'cars/calls'"
  sql_version       = "2015-10-08"

  lambda {
    function_arn    = "${aws_lambda_function.order_handler_lambda.arn}"
  }
}
