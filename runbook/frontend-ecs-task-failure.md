FrontEnd ECS troubleshooting

Symptom:
Frontend ECS tasks repeatedly failed and exited with code 1.

Where found:
ECS → Task logs (CloudWatch)

Root error message:
Invalid options object. Dev Server has been initialized using an options object that does not match the API schema.
options.allowedHosts[0] should be a non-empty string.
Running via react-scripts start.

Interpretation:
React dev server configuration incompatible with ECS/ALB environment. Container exits immediately.
