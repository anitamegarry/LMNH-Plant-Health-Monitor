resource "aws_security_group" "c14_plant_practitioners_security_group" {
  name        = "c14_plant_practitioners_security_group"
  vpc_id      = "vpc-0344763624ac09cb6" 

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  
    cidr_blocks = ["0.0.0.0/0"] 
  }
}