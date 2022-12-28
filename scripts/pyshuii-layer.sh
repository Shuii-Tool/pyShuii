apt-get update -y
apt-get install zip -y

mkdir -p /asset-output/python/lib/python3.9/site-packages/

cp -r pyshuii /asset-output/python/lib/python3.9/site-packages/

cd /asset-output
zip -9 -r layer.zip python
rm -r python