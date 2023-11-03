output "instance_eip" {
    value = aws_eip.quizhero_ip.public_ip
}
