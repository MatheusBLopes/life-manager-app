resource "aws_key_pair" "quizhero_key_pair" {
  key_name   = "quizhero_key_pair"
  public_key = file(var.key_file_path)
}

resource "aws_instance" "quizhero_instance" {
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = aws_subnet.subnet_a.id
  vpc_security_group_ids = [aws_security_group.allow_all.id]
  key_name      = aws_key_pair.quizhero_key_pair.key_name

  user_data = <<-EOF
    #!/bin/bash

    # Update the package list
    sudo yum update

    # Install Docker
    sudo yum install -y docker

    # Start Docker and enable it to start on boot
    sudo systemctl start docker
    sudo systemctl enable docker

    # Add the `ec2-user` user to the `docker` group
    sudo usermod -aG docker ec2-user

    # Create a dedicated directory for the app
    sudo mkdir /home/ec2-user/quizhero

    # Set the owner and permissions for the app directory
    sudo chown ec2-user:ec2-user /home/ec2-user/quizhero
    sudo chmod 755 /home/ec2-user/quizhero
  EOF

  tags = {
    Name = "quizhero-instance"
  }
}


