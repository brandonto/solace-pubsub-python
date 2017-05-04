#! /usr/local/bin/python

#
# This example demonstrates Publishing/Subscribing to a Topic using Solace in
# Python 2.7
#
#

from solClient import *
from solClientMsg import *
import time

def messageReceiveCallback(opaqueSession_p, msg_p, user_p):
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
    sessionFuncInfo.eventInfo.callback_p = solClient_session_eventCallbackFunc_t(eventCallback)
    sessionFuncInfo.eventInfo.user_p = None
    sessionFuncInfo.rxInfo = solClient_session_createRxCallbackFuncInfo_t(None, None)

    sessionProps = (c_char_p * 10)(
            SOLCLIENT_SESSION_PROP_HOST,
            "192.168.132.30",
            SOLCLIENT_SESSION_PROP_VPN_NAME,
            "default",
            SOLCLIENT_SESSION_PROP_USERNAME,
            "helloWorldTutorial",
            None
    )

    #solClient_initialize(SOLCLIENT_LOG_DEBUG, None)
    solClient_initialize()
    print "HelloWorldPub initializing..."

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

    msg_p = solClient_opaqueMsg_pt(None)
    solClient_msg_alloc(byref(msg_p))
    solClient_msg_setDeliveryMode(msg_p, SOLCLIENT_DELIVERY_MODE_DIRECT)

    destination = solClient_destination_t()
    destination.destType = SOLCLIENT_TOPIC_DESTINATION
    destination.dest = c_char_p("tutorial/topic")
    solClient_msg_setDestination(
            msg_p,
            byref(destination),
            sizeof(destination)
    )

    text_p = c_char_p("Hello world!")
    solClient_msg_setBinaryAttachment(
            msg_p,
            text_p,
            len(text_p.value)
    )

    print "About to send message '" + text_p.value + "' to topic '" + destination.dest + "'..."
    solClient_session_sendMsg(session_p, msg_p)

    print "Message sent."
    solClient_msg_free(byref(msg_p))

    print "Exiting."
    solClient_session_disconnect(session_p)

    solClient_cleanup()


if __name__ == "__main__":
    main()

