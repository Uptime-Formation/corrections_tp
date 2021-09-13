import java.text.SimpleDateFormat

currentBuild.displayName = new SimpleDateFormat("yy.MM.dd").format(new Date())


// ###############
env.BASE_DOMAIN = "<votre domaine de base>" // e.g. myjenkinscluster.domain.eu
// ###############

env.REPO_ADDRESS = "https://github.com/Uptime-Formation/corrections_tp.git"
env.REPO_BRANCH = "jenkins_application"
env.REGISTRY_ADDRESS = "registry.${BASE_DOMAIN}"
env.APP_ADDRESS_BETA = "monstericon-beta.${BASE_DOMAIN}"
env.APP_ADDRESS_PROD = "monstericon.${BASE_DOMAIN}"
env.APP_NAME="monstericon"
env.IMAGE = "${env.REGISTRY_ADDRESS}/${env.APP_NAME}"
env.TAG = "${currentBuild.displayName}"
env.TAG_BETA = "${env.TAG}-${env.BRANCH_NAME}"

def nodelabel = "jenkins-k8sagent-${UUID.randomUUID().toString()}"

podTemplate(
  label: nodelabel,
  namespace: "jenkins",
  serviceAccount: "jenkins",
  yaml: """
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: ci
spec:
  containers:
    - name: python
      image: python:3.9
      command:
        - cat
      tty: true
    - name: kubectl
      image: tecpi/kubectl-helm
      command: ["cat"]
      tty: true
"""
) {
  node(nodelabel) {
    stage("unit tests") {
        container('python') {
          git url: "${env.REPO_ADDRESS}", branch: "${env.REPO_BRANCH}"
          sh "pip install -r requirements.txt"
          sh "python -m pytest src/tests/unit_tests.py --verbose"
        }
    }

    node("docker-agent") {
      stage("build") {
        git url: "${env.REPO_ADDRESS}", branch: "${env.REPO_BRANCH}"

        sh "sudo docker image build -t ${env.IMAGE}:${env.TAG_BETA} ."

        sh "sudo docker login ${env.REGISTRY_ADDRESS} -u 'none', -p 'none'"

        sh "sudo docker image push ${env.IMAGE}:${env.TAG_BETA}" // need ingress nginx bodysize 0 for the registry
      }
    }

    stage("functionnal tests") {
      try {
        container("kubectl") {
          sh "env"
          sh "kubectl kustomize k8s/overlays/dev | envsubst | tee manifests.yaml"
          sh "kubectl apply -f manifests.yaml -n jenkins-dev-deploy"
          sh "kubectl -n jenkins-dev-deploy rollout status deployment ${env.APP_NAME}"
        }
        container("python") {
          sh 'echo "nameserver 1.1.1.1" | tee /etc/resolv.conf' // fuck DNS resolution screw with functionnal tests
          sh "python src/tests/functionnal_tests.py http://${APP_ADDRESS_BETA}"
        }
      } catch(e) {
          error "Failed functional tests"
      } finally {
        container("kubectl") {
          sh "kubectl delete -f manifests.yaml -n jenkins-dev-deploy" // uninstall test release
        }
      }
    }

    node("ssh-docker-agent") {
      stage("release") {
        sh "sudo docker pull ${env.IMAGE}:${env.TAG_BETA}"
        sh "sudo docker pull ${env.IMAGE}:latest"

        sh "sudo docker image tag ${env.IMAGE}:${env.TAG_BETA} ${env.IMAGE}:rollback"

        sh "sudo docker image tag ${env.IMAGE}:${env.TAG_BETA} ${env.IMAGE}:${env.TAG}"
        sh "sudo docker image tag ${env.IMAGE}:${env.TAG_BETA} ${env.IMAGE}:latest"

        sh "sudo docker login -u 'none' -p 'none' ${env.REGISTRY_ADDRESS}"

        sh "sudo docker image push ${env.IMAGE}:${env.TAG}"
        sh "sudo docker image push ${env.IMAGE}:latest"
        sh "sudo docker image push ${env.IMAGE}:rollback"
      }
    }

    stage("Production deploy and tests") {
      try {
        container("kubectl") {
          sh "env"
          sh "kubectl kustomize k8s/overlays/prod | envsubst | tee manifests.yaml"
          sh "kubectl apply -f manifests.yaml -n prod"
          sh "kubectl -n prod rollout status deployment ${env.APP_NAME}"
        }
        container("python") {
          sh 'echo "nameserver 1.1.1.1" | tee /etc/resolv.conf' // fuck DNS resolution that screw with functionnal tests
          sh "python src/tests/functionnal_tests.py http://${APP_ADDRESS_BETA}"
        }
      } catch(e) {
          // env.TAG = "rollback"
          // sh "kubectl kustomize k8s/overlays/prod | envsubst | tee manifests.yaml"
          // sh "kubectl apply -f manifests.yaml -n prod"
          // sh "kubectl -n prod rollout status deployment ${env.APP_NAME}"
          error "Failed production tests -> should rollback"
      } finally { // clean images and useless releases etc
        container("kubectl") {
          // cleanup
        }
      }
    }
  }
}