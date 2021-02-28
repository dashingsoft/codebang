set -e

dist=dist.tar.gz
rpath="/var/www/codebang/"

# ruser="root@snsoffice.com"
# rid="~/.ssh/aliyun_id_rsa"

ruser="root@codebang.com"
rid="~/.ssh/codebang_id_rsa"

dst="app"
src="dist"

echo "Create package $dist"
tar czf $dist $src

echo "Upload $src to $ruser:$rpath"
scp -r -i $rid $dist $ruser:$rpath
rm $dist

echo "Create remote $src in the path $rpath"
ssh -i $rid $ruser "cd $rpath; rm -rf $dst; tar xzf $dist; mv $src $dst; rm $dist"
