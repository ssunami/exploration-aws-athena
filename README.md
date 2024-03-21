# term-paper-metcs777
Athena is one of the data analytics services offered that can directly analyze the data stored in S3. This service uses SQL as a coding language, in which data engineers are familiar with, and is compatible with various data formats. Thus, it enables us to efficiently modify and/or analyze the data. In this project, we will be executing a simple task to modify/analyze the data on Athena. In addition, we will write the python code using spark, doing exactly the same task, and compare their performances. This paper aims to explore the usefulness of this technology, as well as pros and cons, through the comparison.

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




