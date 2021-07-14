provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "bucket" {
  # "anagram-fd-testing" is already taken and the name has to be globally unique
  bucket = "anagram-al-testing"
}

resource "aws_lambda_function" "test_csv" {
  role             = "${aws_iam_role.lambda_exec_role.arn}"
  handler          = "anagram.lambda_handler"
  runtime          = "python3.8"
  filename         = "anagram.zip"
  function_name    = "test_csv"
  source_code_hash = "${base64sha256(filebase64("anagram.zip"))}"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.test_csv.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }
}

resource "aws_lambda_permission" "allow_bucket" {
  function_name = aws_lambda_function.test_csv.arn
  source_arn = aws_s3_bucket.bucket.arn
  statement_id = "AllowExecutionFromS3Bucket"
  action = "lambda:InvokeFunction"
  principal = "s3.amazonaws.com"
}

resource "aws_iam_role" "lambda_exec_role" {
  name        = "lambda_exec_anagram"
  path        = "/"
  description = "Allows Lambda Function to call AWS services."


  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "basic" {
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
  role       = aws_iam_role.lambda_exec_role.name
}
