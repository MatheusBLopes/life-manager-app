variable "region" {
  default = "us-east-1"
}

variable "key_file_path" {
    description = "Path to the private key file used to connect to the EC2 instances"
    default     = "./quizhero-prod-key-pair.pub"
}

# Network
variable "vpc_cidr" {
  default = "172.31.0.0/16"
}

variable "public_subnet_cidr" {
  default = "172.31.32.0/20"
}

variable "instance_type" {
  default  = "t2.micro"
}

variable "availability_zone" {
  default = "us-east-1a"
}


variable "ami" {
  default = "ami-0df435f331839b2d6"

}
