# /bin/bash

ftp_conf=/root/lftp_user.conf
log_conf=/root/log.conf
prefix_path=ftp
interval=3600

function check_env() {    
    if [ ! -f "${ftp_conf}" ]; then 
        echo "ftp user conf does not exsit."
        exit -1
    fi
    if [ ! -f "${log_conf}" ]; then 
        echo "log conf does not exsit."
        exit -1
    fi

    if [ -z "${NODE_NAME}" ]; then 
        echo "env NODE_NAME does not exsit."
        exit -1
    fi

    if [ -z "${POD_NAMESPACE}" ]; then 
        echo "env POD_NAMESPACE does not exsit."
        exit -1
    fi

    if [ -z "${POD_NAME}" ]; then 
        echo "env POD_NAME does not exsit."
        exit -1
    fi

    
    if [ ! -z "${INTERVAL}" ]; then 
        echo "interval: ${INTERVAL}"
        interval=${INTERVAL}
    fi
}


function readINI()
{
 FILENAME=$1; SECTION=$2; KEY=$3
 RESULT=`awk -F '=' '/\['$SECTION'\]/{a=1}a==1&&$1~/'$KEY'/{print $2;exit}' $FILENAME`
 echo $RESULT
}


function ftp_send_files() {
    cat ${log_conf} | while read line
    do
        program=$(echo ${line} | awk '{print $1}')
        path=$(echo ${line} | awk '{print $2}')
        # remove double quote
        path=$(sed -e 's/^"//' -e 's/"$//' <<<"${path}")
        remotepath=./${prefix_path}/${NODE_NAME}/${POD_NAMESPACE}/${POD_NAME}/${program}
        command="lftp -c 'open -u ${ftpuser},${ftppass} ${ftphost} ${ftpport}; mkdir -fp ${remotepath}'"
        lftp -c "${command}"

        to_send=""
        for f in $(find $path 2>/dev/null); do
            f_size=$(ls -l ${f} | awk '{print $5}')
            f_name=$(echo ${f##*/})
            remotefile=${remotepath}/${f_name}
            command="lftp -c 'open -u ${ftpuser},${ftppass} ${ftphost} ${ftpport}; ls ${remotefile}'"
            remote_size=$(lftp -c "${command}" | awk '{print $5}')
            if [[ -z "${remote_size}" || ${f_size} -ne ${remote_size} ]]; then
                to_send=${to_send}"$f "
            fi
        done

        if [[ ! -z "${to_send}" ]]; then
            command="lftp -c 'open -u ${ftpuser},${ftppass} ${ftphost} ${ftpport}; mput ${to_send} -O ${remotepath}'"
            echo $command
            lftp -c "${command}"
        fi
    done
}

check_env

ftpuser=$(readINI ${ftp_conf} info ftpuser)
ftppass=$(readINI ${ftp_conf} info ftppass)
ftphost=$(readINI ${ftp_conf} info ftphost)
ftpport=$(readINI ${ftp_conf} info ftpport)

while true
do
    ftp_send_files
    echo "sleep ${interval} seconds"
    sleep ${interval}
done




