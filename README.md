# Exploration of AWS Athena
Athena is one of the data analytics services offered that can directly analyze the data stored in S3. This service uses SQL as a coding language, in which data engineers are familiar with, and is compatible with various data formats. Thus, it enables us to efficiently modify and/or analyze the data. In this project, we will be executing a simple task to modify/analyze the data on Athena. In addition, we will write the python code using spark, doing exactly the same task, and compare their performances. This paper aims to explore the usefulness of this technology, as well as pros and cons, through the comparison.

## Data Set
We use the data set consisting of New York City Taxi trip reports in the Year 2013. The dataset was released under the FOIL (The Freedom of Information Law) and made public by Chris Whong (<https://chriswhong.com/open-data/foil_nyc_taxi/>). 

The attributes and their descriptions are listed as below:
| |Attribute|Description|
|-|---------|-----------|
|0|medallion|Taxi ID|
|1|hack_license|Driver ID|
|2|pickup_datetime|Time when passengers were picked up|
|3|dropoff_datetime|Time when passengers were dropped off|
|4|trip_time_in_secs|Trip time in seconds|
|5|trip_distance|Trip distance in miles|
|6|pickup_longitude|Longitude coordinate of pickup location|
|7|pickup_latitude|Latitude coordinate of pickup location| 
|8|dropoff_longitude|Longitude coordinate of dropoff location|
|9|dropoff_latitude|Latitude coordinate of dropoff location| 
|10|payment_type|Payment method: credit or cash|
|11|fare_amount|Fare amount in dollars|
|12|surcharge|Surcharge in dollars|
|13|mta_tax Tax|in dollars|
|14|tip_amount|Tip amount in dollars|
|15|tolls_amount|Bridge and tunnel tolls in dollars|
|16|total_amount|Total payment amount in dollars|

The data set is in CSV format, separated by comma.

## Tasks
We run simple tasks using the taxi dataset explained above, with both EMR and Athena, and compared the performance. The first task is finding top 10 medallions that have the largest number of taxis. The other task is counting the number of trips for the following trip time categories: less than 10 mins, between 10 and 20 mins, between 20 and 30 mins, and more than 30 mins.

## Environmental Setup
As both of our codes are ran using AWS, create the AWS account

### For code sample 1:
1. Open S3 and create a bucket; the below is the settings for the bucket that we created.
   - General purpose
   - Object ownership: ACL disabled
   - Block Public Access Settings: Block All public access
   - Bucket versioning: Disabled
   - Default encryption
       - Encryption type: SSE-S3
       - Bucket Key: Enable
   - Advanced settings: Disabled
 
3. Open EMR and create a cluster;  below is the settings for the cluster that we created.
   - Name and applications
      - Amazon EMR release: emr-7.0.0
      - Application bundle: Spark 3.5.0, Hadoop 3.3.6
      - Operating system options: Amazon Linux release
      - Check Automatically apply latest Amazon Linux updates
   - Cluster configuration
      - Uniform instance groups
      - Choose “m5.xlarge” for EC2 instance type for Primary, Core, and Task
      - EBS root volume: leave the default values
   - Cluster scaling and provisioning
      - Set cluster size manually
      - Instance size: 3 for task, 1 for core
   - Networking: leave the default settings
   - Cluster termination and node replacement
      - Termination option: Automatically terminate cluster after idle time
      - Idle time: 1:00:00
      - Unhealthy node replacement: Turn on
   - Cluster logs: check “Publish cluster-specific logs to Amazon S3”
   - Security configuration and EC2 key pair: Create key pair if not having it
      - Key pair type: RSA
      - Private key file format: .pem (for Mac) otherwise .ppk
      - Browse key
   - IAM roles
      - Amazon EMR service role: Choose an existing service role -> EMR Default role
      - EC2 instance profile for Amazon EMR: Choose an existing instance profile -> EMR_EC2_Default Role

### For code sample 2:
1. AWS CloudFormation (CloudFormation > Stacks)
   Create a stack with new resources
   
   Step 1. Create stack

   - Prerequisite: Prepare template
        - Template is ready
        - Specify template
        - Template source: Upload a template file
  
   Step 2. Specify template

   - Provide a stack name
   - Parameters
  
   Step 3. Configure stack options

   - Tags: default
   - Permissions: default
   - Stack failure options: default
   - Advanced options: default
   - Check stack status: “CREATE_COMPLETE”
   - Go to “Resources” tab and check to fetch the S3 bucket on “Physical ID”

2. AWS S3 (S3 > Buckets)
- Already created a bucket previous environmental setup on CloudFormation
- Create a folder for datasets
- Create a folder for the results

3. AWS Athena (Athena > Administration > Workgroups)
- Create workgroup
- Workgroup details
- Workgroup name
- Analytics engine
- Choose the type of engine: Apache Spark
- Engine version: PySpark engine version 3
- IAM role configuration: default
- Calculation result settings: Choose an existing S3 location
- Other settings: default
- Tags: default

4. AWS Athena (Amazon Athena > Notebook explorer)
- Select workgroup
- Create notebook

5. AWS IAM (Amazon IAM > Roles)
- Search “AWSAthenaSparkExecutionRole” that matches with Athena workgroup Role ARN
- Add permission: Attach policies
- AWSGlueServiceNotebookRole
- AWSGlueServiceRole
- AWSGlueConsoleFullAccess

6. AWS Glue (Glue > Databases)
- Check the database and tables to fetch the S3 bucket
- To add datasets on Glue databases, “Add table”
  
   Step 1. Set table properties
  
   - Table details - Name, Database: Select a database
   - Table format - Standard AWS Glue table (default)
   - Data store - Select the type of source: S3, Select the type of source: my account, Include path: S3 bucket
   - Data format - Classification: CSV, Delimiter: Comma
  
   Step 2. Choose or define schema
   - Schema - Define or upload schema: Add

## Running Code

### For code sample 1:
- Upload the code sample to the S3 bucket created.
- Upload the taxi dataset to S3 bucket
- Small dataset: in cloud shell,  “aws s3 cp s3://metcs777-sp24/data/taxi-data-sorted-small.csv.bz2 s3://your bucket name”
- Large dataset: in cloud shell,  “aws s3 cp s3://metcs777-sp24/data/taxi-data-sorted-large.csv.bz2 s3://your bucket name”
- Within the EMR cluster, create a step.
   - Type: Spark Application
   - Deploy mode: Cluster mode
   - Application: Browse sample code from S3
   - Arguments: "s3://location of dataset s3://location of result of task1 s3://location of result of task2"

### For code sample 2:

1. Start notebook session on AWS Athena (Athena > Notebook editor)

2. Upload the taxi dataset to S3 bucket
   - Small dataset: in cloud shell,“aws s3 cp s3://metcs777-sp24/data/taxi-data-sorted-small.csv.bz2 s3://your bucket name”
   - Large dataset: in cloud shell,“aws s3 cp s3://metcs777-sp24/data/taxi-data-sorted-large.csv.bz2 s3://your bucket name”

3. Fetch Glue database and assess datasets stored on S3 bucket
   - Check databases on Athena notebook
   - “spark.sql(‘show databases’).show()”

4. Export notebook (Athena > Notebook explorer)
   - Go to “Action” tab and then “Export file”

## Result
We have obtained the same output from those two sample codes, though the computation time was different. It took about 10 mins to execute both tasks using EMR, whereas it took less than 5 mins when we used Athena. Therefore, Athena is much more efficient than using EMR for these type of tasks.

