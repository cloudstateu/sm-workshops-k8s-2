<img src="../../../img/logo.png" alt="Chmurowisko logo" width="200" align="right">
<br><br>
<br><br>
<br><br>

# K8s helm charts

## LAB Overview

#### In this lab you are going to work with helm charts

## Task 1: Search and install existing helm charts

1. Install helm: 
   https://helm.sh/docs/intro/install/   
2. Enter https://artifacthub.io/ and explore available helm charts.
3. Search for wordpress helm from bitnami: https://artifacthub.io/packages/helm/bitnami/wordpress
4. On the right-hand site of a web page you will see **INSTALL** button. Click it and execute commands that appeared.
5. Monitor deployment creation (`kubectl get deployment`) and follow instructions in termimal in order to launch wordpress and log-in to admin console.
6. List all helm releases: `helm list`
7. List all objects that were created for this deployment: `kubectl get all --all-namespaces -l='app.kubernetes.io/managed-by=Helm,app.kubernetes.io/instance=my-wordpress'`
8. You can also get all deployed yamls for wordpress: `helm get manifest my-wordpress`
9. Delete the wordpress release: `helm delete <-wordpress release name->`
10. Make sure it is deleted: `helm list`

## Task 2: Create your own helm chart
In this task you are going to create your own helm chart.
1. Run: `helm create mychart`. This command will create new directory "mychart". Explore the content of "mychart" directory.
2. Take a look on templating engine. Open `templates/service.yaml` and see how template is defined, how "templates/service.yaml" and "values.yaml" are combined.
3. Explore what will be the final yaml generated from template: `helm install --dry-run --debug --generate-name ./mychart`. This command does a dry-run so in fact nothing happed. You can also run `helm template ./mychart` - this command does the same.
4. Take a look and note which port is defined in resulting Service object.
5. Open `values.yaml` and change `service.port` field to `81`
6. Execute `helm install --dry-run --debug --generate-name ./mychart` again and see that service port number has changed.
7. Open `values.yaml` and  back `service.port` field to `80`

## Task 3: Deploy your own helm chart
Generated helm chart deploys nginx in as a ClusterIP service which is accessible only within the cluster. Let's deploy our solution but change:
- application from nginx to TODO app
- service type to LoadBalancer

1. Open `values.yaml`
2. Change `service.type` to `LoadBalancer`
3. Change `image.repository` to `prydonius/todo`
4. Add node selector. Change line 78 to `nodeSelector: {[beta.kubernetes.io/os: linux]}`
5. Open `Chart.yaml` and change `AppVersion` to `1.0.0`. This value is used as a tag for the docker image.
6. Validate your charts with linter: `helm lint ./mychart`
7. Ups... We have an error in our yaml. Node selector (line 78) is bad formatted. Correct it to `nodeSelector: {beta.kubernetes.io/os: linux}`
8. Run `helm lint ./mychart` again. Now it should be ok.
9. Install your solution: `helm install mytodoapp ./mychart`
10. Wait for the deployment to finish and grab the service ip: `kubectl get svc` 
11. Run a TODO app in a browser.
12. Update your helm deployment. This time we will use command line for updating values:
`helm upgrade mytodoapp ./mychart --set replicaCount=3`
13. Check if 2 more pods were created: `kubectl get pods`

## Task 4: Upload your helm chart to ACR
1. You can also make a package from your helm dir: `helm package ./mychart`.
2. Authenticate to ACR (use admin login credentials):
```
helm registry login $ACR_NAME.azurecr.io \
  --username $USER_NAME \
  --password $PASSWORD
```
3. Push to ACR:
```
helm push mychart-0.1.0.tgz oci://$ACR_NAME.azurecr.io/helm
```

## Task 5: Verify your helm chart

1. To check all deployed helm charts to your cluster run:
```
helm ls -n default
```

2. To check all revisions of a specific helm chart (wordpress):
```
helm history mytodoapp -n default
```

3. It's also possible to rollback to a previous revision:

```
helm rollback mytodoapp <version> -n default
```

## Task 6: Delete your helm chart

1. To delete your helm chart run:
```
helm uninstall mytodoapp -n default
```

2. Verify that all resources were deleted:
```
kubectl get all -n default
```

## END LAB

<br><br>

<center><p>&copy; 2023 Cloud Value Professional<p></center>
