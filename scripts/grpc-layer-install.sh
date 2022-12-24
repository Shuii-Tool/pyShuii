yum -y update

# package installation
pip install grpc
pip freeze > requirements.txt
pip install -r requirements.txt -t /asset-output/python/lib/python3.9/site-packages/

# file cleanup

cd /asset-output/python/lib/python3.9/site-packages
rm -r *dist-info
find . | grep -E "(/__pycache__$)" | xargs rm -rf
cd ../../../../

zip -9 -r layer.zip python
rm -r python temp-packages