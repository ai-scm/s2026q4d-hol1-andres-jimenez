# s2026q4d-hol1-andres-jimenez
This repository contains the information from the first Hands on Lab.

Here is the lambda permissions to read and put on the buckets:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-1:891377180652:*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:us-east-1:891377180652:log-group:/aws/lambda/bld-tseed-workshop-andres-jimenez:*"
        },
        {
            "Sid": "ReadSourceBucket",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::bld-tseed-workshop-input-semillero-2026-q4/andres-jimenez/users_dataset_100.csv"
            ]
        },
        {
            "Sid": "WriteOutputBucket",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::bld-tseed-workshop-output-semillero-2026-q4-d/andres-jimenez/*"
            ]
        }
    ]
}
```