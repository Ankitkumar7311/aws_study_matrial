#### Amazon ECR — Detailed Beginner Notes



1\. What is Amazon ECR?



ECR = Elastic Container Registry



Amazon ECR is an AWS service used to store, manage, and deploy Docker container images.



Simple example:



Your Computer

&#x20;    |

&#x20;    | docker build

&#x20;    ↓

Docker Image

&#x20;    |

&#x20;    | docker push

&#x20;    ↓

Amazon ECR

&#x20;    |

&#x20;    | docker pull

&#x20;    ↓

EC2 / ECS / EKS

&#x20;    |

&#x20;    ↓

Container



Think of ECR as GitHub for Docker images.



GitHub → stores source code

ECR → stores Docker images

2\. Why Do We Need ECR?



Suppose you have a Java application.



You create a Docker image:



my-java-app:v1



You want to run this application on an AWS EC2 server.



Instead of manually copying application files, you can:



Developer

&#x20;  ↓

Build Docker Image

&#x20;  ↓

Push Image to ECR

&#x20;  ↓

EC2 pulls Image

&#x20;  ↓

Run Container



This makes deployment easier and consistent.



3\. Important ECR Terms

Term	Meaning

ECR	Elastic Container Registry

Repository	Place where Docker images are stored

Image	Packaged application

Tag	Version/name of an image

Registry	ECR service that stores repositories

Push	Upload image to ECR

Pull	Download image from ECR

Docker	Container platform

URI	Address of an ECR repository

4\. ECR Repository



A repository is like a folder for Docker images.



Example:



ECR

&#x20;|

&#x20;└── my-app

&#x20;     |

&#x20;     ├── v1

&#x20;     ├── v2

&#x20;     └── latest



You can create a repository such as:



my-web-app

5\. ECR Repository URI



After creating a repository, AWS gives you a URI similar to:



123456789012.dkr.ecr.ap-south-1.amazonaws.com/my-web-app



Breakdown:



123456789012

&#x20;     ↓

AWS Account ID



dkr.ecr

&#x20;     ↓

Amazon ECR



ap-south-1

&#x20;     ↓

AWS Region



my-web-app

&#x20;     ↓

Repository



Your actual URI will be different.



6\. ECR Architecture

&#x20;                   AWS

&#x20;                    |

&#x20;                   ECR

&#x20;                    |

&#x20;             ┌──────────────┐

&#x20;             │  Repository  │

&#x20;             │   my-app     │

&#x20;             └──────────────┘

&#x20;                    |

&#x20;         ┌──────────┼──────────┐

&#x20;         ↓          ↓          ↓

&#x20;       :v1        :v2       :latest

&#x20;         |

&#x20;         ↓

&#x20;      Docker Image

7\. Prerequisites



For this practical, you need:



AWS account

AWS CLI

Docker

ECR repository

IAM permissions

Internet connection

8\. Check AWS CLI



On your computer:



aws --version



Example:



aws-cli/2.x.x



If AWS CLI is configured:



aws sts get-caller-identity



This confirms which AWS account you are connected to.



9\. Check Docker



Run:



docker --version



Example:



Docker version 28.x.x



If Docker is installed correctly, the command will return the version.



10\. Configure AWS CLI



If you haven't configured AWS CLI:



aws configure



It asks:



AWS Access Key ID:

AWS Secret Access Key:

Default region name:

Default output format:



For example:



AWS Access Key ID: YOUR\_ACCESS\_KEY

AWS Secret Access Key: YOUR\_SECRET\_KEY

Default region name: ap-south-1

Default output format: json



Never share your access key or secret key with anyone.



11\. Create ECR Repository



You can create it from the AWS Console:



AWS Console

&#x20;  ↓

ECR

&#x20;  ↓

Repositories

&#x20;  ↓

Create repository



Repository name:



my-web-app



Keep other settings at their defaults for this basic practice.



Click:



Create repository

12\. Create ECR Repository Using CLI



You can also create it using:



aws ecr create-repository \\

&#x20;   --repository-name my-web-app \\

&#x20;   --region ap-south-1



Check:



aws ecr describe-repositories \\

&#x20;   --repository-names my-web-app \\

&#x20;   --region ap-south-1

13\. Create a Simple Application



Create a project folder:



mkdir my-web-app



Go inside:



cd my-web-app



Create:



index.html



Example:



<!DOCTYPE html>

<html>

<head>

&#x20;   <title>My ECR App</title>

</head>

<body>

&#x20;   <h1>Hello from Docker + ECR</h1>

</body>

</html>

14\. Create Dockerfile



Inside the project directory:



my-web-app/

│

├── index.html

└── Dockerfile



Create Dockerfile:



vim Dockerfile



Add:



FROM nginx:latest



COPY index.html /usr/share/nginx/html/index.html



EXPOSE 80



Save:



Esc

:wq

Enter

15\. Understand Dockerfile

FROM

FROM nginx:latest



This uses the Nginx Docker image as the base image.



COPY

COPY index.html /usr/share/nginx/html/index.html



Copies your HTML file into the Nginx container.



EXPOSE

EXPOSE 80



Documents that the container application uses port 80.



16\. Build Docker Image



From the project directory:



docker build -t my-web-app:v1 .



Explanation:



docker build

&#x20;    ↓

Build image



\-t

&#x20;    ↓

Give image a name/tag



my-web-app:v1

&#x20;    ↓

Image name + version



.

&#x20;    ↓

Current directory

17\. Check Docker Image

docker images



You should see something like:



REPOSITORY    TAG    IMAGE ID

my-web-app    v1     abc123...

18\. Run Container Locally



Before pushing to ECR, test your image.



docker run -d -p 8080:80 --name my-web-container my-web-app:v1



Explanation:



\-p 8080:80



means:



Host Port       Container Port

&#x20;  8080    →        80

19\. Check Container

docker ps



You should see:



my-web-container



Test in browser:



http://localhost:8080



You should see:



Hello from Docker + ECR

20\. Stop Container



After testing:



docker stop my-web-container



Remove it:



docker rm my-web-container

21\. Authenticate Docker with ECR



Now we need to allow Docker to communicate with ECR.



Run:



aws ecr get-login-password --region ap-south-1 | \\

docker login --username AWS --password-stdin \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com



Expected:



Login Succeeded



Replace:



YOUR\_ACCOUNT\_ID



with your AWS Account ID.



22\. Find Your AWS Account ID



Run:



aws sts get-caller-identity --query Account --output text



Example:



123456789012

23\. Get ECR Repository URI



Run:



aws ecr describe-repositories \\

&#x20;   --repository-names my-web-app \\

&#x20;   --region ap-south-1 \\

&#x20;   --query 'repositories\[0].repositoryUri' \\

&#x20;   --output text



Example output:



123456789012.dkr.ecr.ap-south-1.amazonaws.com/my-web-app

24\. Tag Docker Image



Currently your image is:



my-web-app:v1



ECR needs the image tagged with the repository URI.



Run:



docker tag my-web-app:v1 \\

123456789012.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1



Check:



docker images



Now you should see both:



my-web-app:v1



and:



123456789012.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1



Both point to the same underlying image.



25\. Push Image to ECR



Now upload the image:



docker push \\

123456789012.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1



You will see Docker uploading layers.



At the end, you should get a digest similar to:



latest: digest: sha256:...

26\. Verify Image in ECR



AWS Console:



ECR

&#x20;↓

Repositories

&#x20;↓

my-web-app

&#x20;↓

Images



You should see:



Tag: v1



Your Docker image is now stored in AWS ECR.



27\. Pull Image from ECR



On another machine/server, first authenticate:



aws ecr get-login-password --region ap-south-1 | \\

docker login --username AWS --password-stdin \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com



Then:



docker pull \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1

28\. Run ECR Image on EC2



Suppose you have an Ubuntu EC2 instance.



Install Docker on EC2 first.



Then authenticate:



aws ecr get-login-password --region ap-south-1 | \\

docker login --username AWS --password-stdin \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com



Pull:



docker pull \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1



Run:



docker run -d \\

\-p 80:80 \\

\--name my-web-container \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1

29\. Final Deployment Architecture

&#x20;             Developer

&#x20;                 |

&#x20;                 |

&#x20;           Docker Build

&#x20;                 |

&#x20;                 ↓

&#x20;            Docker Image

&#x20;                 |

&#x20;                 |

&#x20;            docker push

&#x20;                 |

&#x20;                 ↓

&#x20;       ┌───────────────────┐

&#x20;       │    Amazon ECR     │

&#x20;       │                   │

&#x20;       │    my-web-app     │

&#x20;       │       :v1         │

&#x20;       └───────────────────┘

&#x20;                 |

&#x20;                 |

&#x20;            docker pull

&#x20;                 |

&#x20;                 ↓

&#x20;            EC2 Instance

&#x20;                 |

&#x20;                 ↓

&#x20;             Container

&#x20;                 |

&#x20;                 ↓

&#x20;              Nginx

&#x20;                 |

&#x20;                 ↓

&#x20;            index.html

&#x20;                 |

&#x20;                 ↓

&#x20;              Browser

30\. ECR + EC2 Practical Flow



Remember these 8 steps:



1\. Create Dockerfile

&#x20;       ↓

2\. Build Docker Image

&#x20;       ↓

3\. Create ECR Repository

&#x20;       ↓

4\. Login Docker to ECR

&#x20;       ↓

5\. Tag Docker Image

&#x20;       ↓

6\. Push Image to ECR

&#x20;       ↓

7\. EC2 Login to ECR

&#x20;       ↓

8\. Pull \& Run Container

31\. Complete Command Sequence



For quick practice, the complete flow is:



Create repository

aws ecr create-repository \\

\--repository-name my-web-app \\

\--region ap-south-1

Build image

docker build -t my-web-app:v1 .

Login

aws ecr get-login-password --region ap-south-1 | \\

docker login --username AWS --password-stdin \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com

Tag

docker tag my-web-app:v1 \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1

Push

docker push \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1

Pull

docker pull \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1

Run

docker run -d \\

\-p 80:80 \\

\--name my-web-container \\

YOUR\_ACCOUNT\_ID.dkr.ecr.ap-south-1.amazonaws.com/my-web-app:v1

32\. Useful ECR Commands

List repositories

aws ecr describe-repositories

List images

aws ecr list-images \\

\--repository-name my-web-app

Delete image

aws ecr batch-delete-image \\

\--repository-name my-web-app \\

\--image-ids imageTag=v1

Delete repository

aws ecr delete-repository \\

\--repository-name my-web-app \\

\--force



⚠️ --force deletes the repository and its images.



33\. ECR vs Docker Hub

Feature	ECR	Docker Hub

Provider	AWS	Docker

Integration	AWS services	Docker ecosystem

Private repositories	Yes	Yes

Public repositories	Yes	Yes

IAM integration	Yes	Different authentication model

Best for	AWS deployments	General Docker sharing



For an AWS project, ECR is especially useful because it integrates naturally with services such as EC2, ECS, EKS, and other AWS deployment workflows.



34\. Important Interview Questions

Q1. What is ECR?



Amazon Elastic Container Registry is a managed AWS service for storing and managing Docker/container images.



Q2. What is an ECR repository?



A repository is a storage location for container images.



Q3. What is docker push?



It uploads a Docker image to a registry such as ECR.



Q4. What is docker pull?



It downloads an image from a registry.



Q5. Why do we tag an image?



To identify the image repository and version.



Example:



my-web-app:v1

Q6. What does :v1 mean?



It is the image tag, commonly used to identify a version.



Q7. What is the difference between ECR and EC2?

ECR → Stores container images



EC2 → Runs virtual servers

Q8. Can EC2 pull an image from ECR?



Yes, provided the EC2 environment has the required AWS permissions and Docker/ECR authentication.



35\. Most Important Concept



Don't confuse these three:



Docker

&#x20;  ↓

Builds and runs containers/images



ECR

&#x20;  ↓

Stores container images



EC2

&#x20;  ↓

Provides virtual server where containers can run



So the overall concept is:



Docker Image

&#x20;    ↓

&#x20;   ECR

&#x20;    ↓

&#x20;   EC2

&#x20;    ↓

&#x20;Docker Container

&#x20;    ↓

&#x20;Application



This is the basic Docker → ECR → EC2 deployment workflow you should remember.

