#!/bin/bash
# zip the html pages and corresponding data

# check if proposed parent dir exists, otherwise produce it
PDIR=$1

[[ ! -d ${PDIR} ]] && mkdir ${PDIR}

for FL in `ls ../acanthis | grep -v 'images_'`
do
	[[ ! -d "${PDIR}/acanthis/" ]] && mkdir "${PDIR}/acanthis/"
	cp -r "../acanthis/${FL}" "${PDIR}/acanthis"	
done

for FL in `ls ../acanthis/images_std | grep -v 'raw' | grep -v 'csv'`
do
	[[ ! -d "${PDIR}/acanthis/images_std" ]] && mkdir "${PDIR}/acanthis/images_std"
	cp -r "../acanthis/images_std/${FL}" "${PDIR}/acanthis/images_std"	
done

[[ ! -d "${PDIR}/meta" ]] && mkdir "${PDIR}/meta"
[[ ! -d "${PDIR}/public" ]] && mkdir "${PDIR}/public"
cp -r ../meta/* "${PDIR}/meta/"
cp -r ../public/* "${PDIR}/public/"

# zip -r -Z bzip2 "${PDIR}.zip" ${PDIR}

# rm -r ${PDIR}
echo "Webpage was exported to ${PDIR}."
