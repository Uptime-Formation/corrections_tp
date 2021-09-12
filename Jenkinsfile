import java.text.SimpleDateFormat

currentBuild.displayName = new SimpleDateFormat("yy.MM.dd").format(new Date()) + "-" + env.BUILD_NUMBER

env.REPO_ADDRESS = "https://github.com/Uptime-Formation/corrections_tp.git"
env.REPO_BRANCH = "jenkins_application"
env.BASE_DOMAIN = "v3s2.dopl.uk"
env.REGISTRY_ADDRESS = "registry.${BASE_DOMAIN}"
env.APP_ADDRESS_BETA = "monstericon-beta.${BASE_DOMAIN}"
env.APP_NAME="monstericon"
env.IMAGE = "${env.REGISTRY_ADDRESS}/${env.APP_NAME}"
// env.ADDRESS = "go-demo-3-${env.BUILD_NUMBER}-${env.BRANCH_NAME}.acme.com"
// env.PROD_ADDRESS = "go-demo-3.acme.com"
env.TAG = "${currentBuild.displayName}"
env.TAG_BETA = "${env.TAG}-${env.BRANCH_NAME}"

// def nodelabel = "jenkins-k8sagent-${UUID.randomUUID().toString()}"

podTemplate(
  // label: nodelabel,
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

    node("ssh-docker-agent") {
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
          // sh "kubectl create namespace beta"
          // sh "kubectl get nodes"
          sh "env"
          sh "kubectl kustomize k8s/overlays/dev | envsubst | tee manifests.yaml"
          sh "kubectl apply -f g manifests.yaml"
          sh "kubectl -n jenkins rollout status ${env.APP_NAME}"
        }
        container("python") {
          sh "python src/tests/functionnal_tests.py "
        }
      } catch(e) {
          error "Failed functional tests"
      } finally {
        container("kubectl") {
          sh "kubectl get pods -n jenkins"
        }
      }
    }
  }
}
//     node("docker") {
//       stage("release") {
//         sh "sudo docker pull ${env.IMAGE}:${env.TAG_BETA}"
//         sh "sudo docker image tag ${env.IMAGE}:${env.TAG_BETA} ${env.IMAGE}:${env.TAG}"
//         sh "sudo docker image tag ${env.IMAGE}:${env.TAG_BETA} ${env.IMAGE}:latest"

//         sh "sudo docker login -u 'none' -p 'none' ${env.REGISTRY_ADDRESS}"

//         sh "sudo docker image push ${env.IMAGE}:${env.TAG}"
//         sh "sudo docker image push ${env.IMAGE}:latest"
//       }
//     }
//   }
// }