#!/usr/bin/env zsh
#
# stop on error
set -e

if [ `git rev-parse --abbrev-ref HEAD` != "dev" ]; then
    echo "Just publish from the dev branch!!!!"
    return -1
fi

# build page
./site.py build


# resize images
for f in build/static/photos/**/*jpg
do
    convert "$f" -resize 2048x2048 -interlace Plane "$f"
done

# to gh-pages

git remote update

WD=`pwd`
TARGETDIR=`mktemp -du`
git clone $WD $TARGETDIR
cd $TARGETDIR
git checkout master
rm -r *
cp -r $WD/build/* .
git add .
git commit -m "publish site"

git push origin master

echo "Now do a git push to send changes to the github repository!"
