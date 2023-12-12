<img src="../../../img/logo.png" alt="CVP logo" width="200" align="right">
<br><br>
<br><br>
<br><br>

# Kubernetes operators

## LAB Overview

In this lab, you will learn how to deploy various kubernetes applications using Operator's pattern.

## Task 1: Install PostgreSQL Operator and PostgeSQL Operator UI
1. Instalation using helm:
    
    ```bash
    # add repo for postgres-operator
    helm repo add postgres-operator-charts https://opensource.zalando.com/postgres-operator/charts/postgres-operator

    # install the postgres-operator
    helm install postgres-operator postgres-operator-charts/postgres-operator

    # add repo for postgres-operator-ui
    helm repo add postgres-operator-ui-charts https://opensource.zalando.com/postgres-operator/charts/postgres-operator-ui

    # install the postgres-operator-ui
    helm install postgres-operator-ui postgres-operator-ui-charts/postgres-operator-ui
    ```

2. Check if operator is running:

    ```bash
    kubectl get pod -l app.kubernetes.io/name=postgres-operator
    ```

3. Check id operator UI is running:
    
    ```bash
    kubectl get pod -l app.kubernetes.io/name=postgres-operator-ui
    ```
4. Forward port to UI:
   
    ```bash
    kubectl port-forward svc/postgres-operator-ui 8081:80
    ```
    
    and access it on http://localhost:8081/

## Task 2: Create new postgres cluster using UI
1. At to top bar of UI click *New Cluster* and fill in the form. Set cluster name, 2 instances and you can leave other fields by default. Then click *Create cluster*.

## Task 3: Create new postgres cluster using YAML definition
1. Examine the content of "files/pg_cluster.yaml".

   **Enter database name in line 21 and a username in lines 12 and 21**
   
3. Deploy new cluster:
    
    ```bash
    kubectl apply -f pg_cluster.yaml
    ```

4. Wait for new pods to be deployed:
    
    ```bash
    kubectl get pods
    ```

5. Examine what resources have been created:
    
    ```bash
    kubectl get all
    ```

6. Get name of master node from a cluster:
    
    ```bash
    export PGMASTER=$(kubectl get pods -o jsonpath={.items..metadata.name} -l application=spilo,cluster-name=acid-minimal-cluster,spilo-role=master -n default)
    ```

7. Get password to PostgreSQL database:
    
    ```bash
    kubectl get secret postgres.clouds-demo-cluster.credentials.postgresql.acid.zalan.do -o 'jsonpath={.data.password}' | base64 -d
    ```

8. In new terminal windows run a pod with psql:
    
    ```bash
    kubectl run -it --rm psql-test --image=postgres:15 -- bash
    ```

9. And connect to Postgres database:
    
    ```bash
    export PGPASSWORD=<YOUR_PG_PASSWORD>
    psql -U postgres -h clouds-demo-cluster -p 5432
    ```

10. Type `\l` and check if your database exists.
11. Delete your databases using UI.
12. Uninstall operators:
    
    ```bash
    helm uninstall postgres-operator-ui
    helm uninstall postgres-operator
    ```

## END LAB

<br><br>


<center><p>&copy; 2023 Cloud Value Professional<p></center>
