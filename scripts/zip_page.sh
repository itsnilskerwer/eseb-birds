#!/bin/bash
# zip the html pages and corresponding data

# check if proposed parent dir exists, otherwise produce it
PDIR=$1

[[ ! -d ${PDIR} ]] && mkdir ${PDIR}

for FL in `ls ../data | grep -v 'images_'`
do
	[[ ! -d "${PDIR}/data/" ]] && mkdir "${PDIR}/data/"
	cp -r "../data/${FL}" "${PDIR}/data"	
done

for FL in `ls ../data/images_std | grep -v 'raw' | grep -v 'csv'`
do
	[[ ! -d "${PDIR}/data/images_std" ]] && mkdir "${PDIR}/data/images_std"
	cp -r "../data/images_std/${FL}" "${PDIR}/data/images_std"	
done

[[ ! -d "${PDIR}/meta" ]] && mkdir "${PDIR}/meta"
[[ ! -d "${PDIR}/public" ]] && mkdir "${PDIR}/public"
cp -r ../meta/* "${PDIR}/meta/"
cp -r ../public/* "${PDIR}/public/"

# zip -r -Z bzip2 "${PDIR}.zip" ${PDIR}

# rm -r ${PDIR}
echo "Webpage was exported to ${PDIR}."
