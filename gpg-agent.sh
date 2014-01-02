#!/bin/sh

# Skip processing this file if it's not a regular user or root.
# We cannot use exit because this file is likely sourced.
if [[ $UID -lt 500 ]] ; then
	. /etc/sysconfig/gnupg
	if [[ ! -n "$GPG_AGENT_INFO" && "$START_GPGAGENT" = "yes" && \
		-s /etc/mtab && \
		"`echo $GPG_AGENT_NO_USERS | grep \ $UID\  ; echo $?`" -ne 0 && \
		! -e $HOME/.gnupg/gpg-agent-no-start ]] ; then
		
		if [[ "$START_GPGAGENT_SH" = "yes" ]] ; then
			GPGAGENTINFO="$HOME/.gnupg/gpg-agent-info"
			NEEDSTART=0
			if [ -f "$GPGAGENTINFO" ] ; then
				kill -0 `cut -d: -f 2 "$GPGAGENTINFO"` 2>/dev/null
			       	if [ $? -eq 0 ] ; then
					. "$GPGAGENTINFO"
					export GPG_AGENT_INFO
				else
					NEEDSTART=1
				fi # 
			else
				rm -f "$GPGAGENTINFO"
				NEEDSTART=1
			fi # -f "$GPGAGENTINFO"
			if [ ${NEEDSTART} -eq 1 ] ; then
				if [[ ! -n $GPGAGENT_PARAMS ]] ; then 
					GPGAGENT_PARAMS="--keep-display"
				fi
				eval `gpg-agent ${GPGAGENT_PARAMS} --daemon --write-env-file "$GPGAGENTINFO"`
			fi # NEEDSTART
		fi # START_GPGAGENT_SH
	fi # BIG conditional list
fi # End of UID clause.
