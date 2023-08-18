# My Project CI/CD with GitHub Actions

This repository contains the source code and configuration for automating the Continuous Integration and Continuous Deployment (CI/CD) process using GitHub Actions. The workflow is designed to build and deploy a Docker image of my project whenever changes are pushed to the `main` branch.

## Workflow Overview

The GitHub Actions workflow performs the following steps:

1. **Install Dependencies and Setup Environment:**
   - Install necessary dependencies and configure the environment.
   - Set up SSH key for remote server access (if applicable).

2. **Retrieve Data from DVC:**
    - Log in to DVC using provided credentials.
    - Pull data from DVC remote storage.

2. **Build Docker Image:**
   - Build a Docker image from the source code.
   - Tag the image appropriately.

3. **Push Docker Image:**
   - Log in to DockerHub using provided credentials.
   - Push the Docker image to a DockerHub repository.

## How to Use

1. **Repository Setup:**
   - Clone this repository to your local machine: `git clone https://github.com/aguschin/art-guide.git`

2. **Configuration:**
   - Configure your DVC and Docker settings in your project as needed.
   - Update `.github/workflows/ci-cd.yml` with your specific project details.

3. **GitHub Secrets:**
   - In your GitHub repository settings, go to "Settings" > "Secrets".
   - Add the following secrets:
     - `DOCKERHUB_USERNAME`: Your DockerHub username.
     - `DOCKERHUB_PASSWORD`: Your DockerHub password or access token.
     - `SSH_PRIVATE_KEY`: Your SSH private key for server access (if applicable).

4. **Push Changes:**
   - Make changes to your project code and push them to the `main` branch. (the recommendation is to do it by creating a Pull Request)

5. **Workflow Execution:**
   - The GitHub Actions workflow will be triggered automatically on every push and pull request to the `main` branch.
   - The workflow will install dependencies, retrieve needed data, build the Docker image, and push it to DockerHub.
   - If you have configured SSH for server deployment, the workflow will also deploy the image to your server.

## Future Work
    - Add custom tags to the image.
    - Create testing bot and API and then add a job (Test) to pull and run image and test.
    - Create script in server to pull the image and run it and then add a new job (Deploy) to run the script.

## Notes

- The workflow can be customized further to include additional steps such as testing, deployment, linting, and more.
- Always ensure the security of your credentials and keys by using GitHub Secrets and following best practices.

For more information about GitHub Actions and customizing workflows, refer to the official GitHub Actions documentation: [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**License:** This project is licensed under the [MIT License](LICENSE).
