yum -y update

# packages
yum -y install base-devel wget

# mbedtls install
bash mbedtls-install.sh

# add epel repo
#yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && yum-config-manager --enable epel

# package installation
pip install poetry
poetry export -f requirements.txt --without-hashes > requirements.txt
pip install -r requirements.txt -t /asset-output/python/lib/python3.9/site-packages/

cp -r pyshuii /asset-output/python/lib/python3.9/site-packages/

# file cleanup
cd /asset-output/python/lib/python3.9/site-packages
# rm -r grpc googleapiclient google netaddr cytoolz coincurve
rm -r *dist-info
find . | grep -E "(/__pycache__$)" | xargs rm -rf
cd -

zip -9 -r primary-layer.zip python
rm -r python