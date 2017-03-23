#! /usr/local/bin/python

#
# This example demonstrates Publishing/Subscribing to a Topic using Solace in
# Python 2.7
#
#

from solClient import *
import time

msgCount_g = 0

def messageReceiveCallback(opaqueSession_p, msg_p, user_p):
    print "Received message:"
    libsolclient.solClient_msg_dump(msg_p, None, 0)
    global msgCount_g
    msgCount_g = msgCount_g + 1
    return 0

def eventCallback(opaqueSession_p, eventInfo_p, user_p):
    print "Session EventCallback() called:  " + str(libsolclient.solClient_session_eventToString(eventInfo_p.contents.sessionEvent))
    return 0

def main():

    # Context variables
    context_p = solClient_opaqueContext_pt(None)
    contextFuncInfo = solClient_context_createFuncInfo_t()
    contextFuncInfo.regFdInfo = solClient_context_createRegisterFdFuncInfo_t(None, None, None)

    # Session variables
    session_p = solClient_opaqueSession_pt(None)
    sessionFuncInfo = solClient_session_createFuncInfo_t()
    sessionFuncInfo.rxMsgInfo = solClient_session_createRxMsgCallbackFuncInfo_t(cast(solClient_session_rxMsgCallbackFunc_t(messageReceiveCallback), c_void_p), None)
    sessionFuncInfo.eventInfo = solClient_session_createEventCallbackFuncInfo_t()
    sessionFuncInfo.eventInfo.callback = solClient_session_eventCallbackFunc_t(eventCallback)
    sessionFuncInfo.eventInfo.user_p = None
    sessionFuncInfo.rxInfo = solClient_session_createRxCallbackFuncInfo_t(None, None)

    sessionProps = (c_char_p * 10)(
            SOLCLIENT_SESSION_PROP_HOST,
            "192.168.132.40",
            SOLCLIENT_SESSION_PROP_VPN_NAME,
            "default",
            SOLCLIENT_SESSION_PROP_USERNAME,
            "helloWorldTutorial",
            None
    )

    #solClient_initialize(SOLCLIENT_LOG_DEBUG, None)
    solClient_initialize()
    print "HelloWorldSub initializing..."

    solClient_context_create(
            SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD,
            byref(context_p),
            byref(contextFuncInfo),
            sizeof(contextFuncInfo)
    )

    solClient_session_create(
            cast(sessionProps, POINTER(c_char_p)),
            context_p,
            byref(session_p),
            byref(sessionFuncInfo),
            sizeof(sessionFuncInfo)
    )

    solClient_session_connect(session_p)
    print "Connected."

    solClient_session_topicSubscribeExt(
            session_p,
            SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM,
            c_char_p("tutorial/topic")
    )

    print "Waiting for message......"
    while msgCount_g < 1:
        time.sleep(1)
        pass

    solClient_session_topicSubscribeExt(
            session_p,
            SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM,
            c_char_p("tutorial/topic")
    )

    print "Exiting."
    solClient_session_disconnect(session_p)

    solClient_cleanup()


if __name__ == "__main__":
    main()

