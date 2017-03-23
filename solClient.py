#! /usr/local/bin/python

#
# This module exposes part of the Solace Messaging C API to Python 2.7
#
#


from ctypes import *

libsolclient = cdll.LoadLibrary('lib/libsolclient.so.1')

(SOLCLIENT_LOG_EMERGENCY,
 SOLCLIENT_LOG_ALERT,
 SOLCLIENT_LOG_CRITICAL,
 SOLCLIENT_LOG_ERROR,
 SOLCLIENT_LOG_WARNING,
 SOLCLIENT_LOG_NOTICE,
 SOLCLIENT_LOG_INFO,
 SOLCLIENT_LOG_DEBUG) = map(c_int, xrange(8))

SOLCLIENT_LOG_DEFAULT_FILTER = SOLCLIENT_LOG_NOTICE

SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD = pointer(
    c_char_p.in_dll(libsolclient, "_solClient_contextPropsDefaultWithCreateThread")
)

SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM = c_int(2)


solClient_opaqueContext_pt  = c_void_p
solClient_opaqueSession_pt  = c_void_p
solClient_opaqueMsg_pt      = c_void_p


#
#  typedef struct solClient_context_createRegisterFdFuncInfo
#  {
#    solClient_context_registerFdFunc_t regFdFunc_p;
#    solClient_context_unregisterFdFunc_t unregFdFunc_p;
#    void *user_p;
#  } solClient_context_createRegisterFdFuncInfo_t;
#
#  typedef struct solClient_context_createFuncInfo
#  {
#    solClient_context_createRegisterFdFuncInfo_t regFdInfo;
#  } solClient_context_createFuncInfo_t;
#

class solClient_context_createRegisterFdFuncInfo_t(Structure):
    _fields_ = [
        ("regFdFunc_p", c_void_p),
        ("unregFdFunc_p", c_void_p),
        ("user_p", c_void_p)
    ]

class solClient_context_createFuncInfo_t(Structure):
    _fields_ = [
        ("regFdInfo", solClient_context_createRegisterFdFuncInfo_t)
    ]

#
#  typedef struct solClient_session_createRxCallbackFuncInfo
#  {
#    void *callback_p;
#    void *user_p;
#  } solClient_session_createRxCallbackFuncInfo_t;
#
#  typedef struct solClient_session_eventCallbackInfo
#  {
#    solClient_session_event_t sessionEvent;         /**< The Session event that has occurred. */
#    solClient_session_responseCode_t responseCode;  /**< A response code that is returned for some events, otherwise zero. */
#    const char *info_p;                             /**< Except for ::SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT (see Detailed Description above), a pointer to a NULL-terminated string providing further information about the event, when available. This pointer is never NULL */
#    void       *correlation_p;                      /**< Application-supplied correlation pointer where applicable. Used when acknowledging or rejecting Guaranteed messages, in responses to any function calls that pass a correlationTag that will be returned in a Session Event. */
#  } solClient_session_eventCallbackInfo_t, *solClient_session_eventCallbackInfo_pt; /**< A pointer to ::solClient_session_eventCallbackInfo structure of information returned with a Session event. */
#
#  typedef void (*solClient_session_eventCallbackFunc_t) (solClient_opaqueSession_pt opaqueSession_p, solClient_session_eventCallbackInfo_pt eventInfo_p, void *user_p);
#
#  typedef struct solClient_session_createEventCallbackFuncInfo
#  {
#    solClient_session_eventCallbackFunc_t callback_p;
#    void *user_p;
#  } solClient_session_createEventCallbackFuncInfo_t;
#
#  typedef struct solClient_session_createRxCallbackFuncInfo
#  {
#    void *callback_p;
#    void *user_p;
#  } solClient_session_createRxCallbackFuncInfo_t;
#
#  typedef struct solClient_session_createFuncInfo
#  {
#    solClient_session_createRxCallbackFuncInfo_t    rxInfo;
#    solClient_session_createEventCallbackFuncInfo_t eventInfo;
#    solClient_session_createRxMsgCallbackFuncInfo_t rxMsgInfo;
#  } solClient_session_createFuncInfo_t;
#

class solClient_session_createRxCallbackFuncInfo_t(Structure):
    _fields_ = [
        ("callback", c_void_p),
        ("user_p", c_void_p)
    ]

class solClient_session_eventCallbackInfo_t(Structure):
    _fields_ = [
        ("sessionEvent", c_void_p),
        ("responseCode", c_void_p),
        ("info_p", c_char_p),
        ("correlation_p", c_void_p)
    ]

solClient_session_eventCallbackInfo_pt = POINTER(solClient_session_eventCallbackInfo_t)

solClient_session_eventCallbackFunc_t = CFUNCTYPE(c_int, solClient_opaqueSession_pt, solClient_session_eventCallbackInfo_pt, c_void_p)
class solClient_session_createEventCallbackFuncInfo_t(Structure):
    _fields_ = [
        ("callback", solClient_session_eventCallbackFunc_t),
        ("user_p", c_void_p)
    ]

solClient_session_rxMsgCallbackFunc_t = CFUNCTYPE(c_int, solClient_opaqueSession_pt, solClient_opaqueMsg_pt, c_void_p)
class solClient_session_createRxMsgCallbackFuncInfo_t(Structure):
    _fields_ = [
        ("callback", c_void_p),
        ("user_p", c_void_p)
    ]

class solClient_session_createFuncInfo_t(Structure):
    _fields_ = [
        ("rxInfo", solClient_session_createRxCallbackFuncInfo_t),
        ("eventInfo", solClient_session_createEventCallbackFuncInfo_t),
        ("rxMsgInfo", solClient_session_createRxMsgCallbackFuncInfo_t)
    ]

SOLCLIENT_SESSION_PROP_USERNAME = c_char_p("SESSION_USERNAME")
SOLCLIENT_SESSION_PROP_HOST     = c_char_p("SESSION_HOST")
SOLCLIENT_SESSION_PROP_VPN_NAME = c_char_p("SESSION_VPN_NAME")

#
# solClient_dllExport solClient_returnCode_t
#   solClient_initialize (solClient_log_level_t initialLogLevel,
#                         solClient_propertyArray_pt props);
#

def solClient_initialize(initialLogLevel=SOLCLIENT_LOG_DEFAULT_FILTER, props=None):
    libsolclient.solClient_initialize(initialLogLevel, props)

#
# solClient_dllExport solClient_returnCode_t
#   solClient_context_create (solClient_propertyArray_pt props,
#                             solClient_opaqueContext_pt * opaqueContext_p,
#                             solClient_context_createFuncInfo_t * funcInfo_p,
#                             size_t funcInfoSize);
#

def solClient_context_create(props, opaqueContext_p, funcInfo_p, funcInfoSize):
    libsolclient.solClient_context_create(props, opaqueContext_p, funcInfo_p, funcInfoSize)

#
# solClient_dllExport solClient_returnCode_t
#   solClient_session_create (solClient_propertyArray_pt props,
#                             solClient_opaqueContext_pt opaqueContext_p,
#                             solClient_opaqueSession_pt * opaqueSession_p,
#                             solClient_session_createFuncInfo_t * funcInfo_p,
#                             size_t funcInfoSize);
#

def solClient_session_create(props, opaqueContext_p, opaqueSession_p, funcInfo_p, funcInfoSize):
    libsolclient.solClient_session_create(props, opaqueContext_p, opaqueSession_p, funcInfo_p, funcInfoSize)

#
# solClient_dllExport solClient_returnCode_t
#   solClient_session_connect (solClient_opaqueSession_pt opaqueSession_p);
#
def solClient_session_connect(opaqueSession_p):
    libsolclient.solClient_session_connect(opaqueSession_p)

#
# solClient_dllExport solClient_returnCode_t
#   solClient_session_disconnect (solClient_opaqueSession_pt opaqueSession_p);
#
def solClient_session_disconnect(opaqueSession_p):
    libsolclient.solClient_session_disconnect(opaqueSession_p)

#
# solClient_dllExport solClient_returnCode_t
#   solClient_session_topicSubscribeExt (
#                                     solClient_opaqueSession_pt opaqueSession_p,
#                                     solClient_subscribeFlags_t flags,
#                                     const char *topicSubscription_p);
#
def solClient_session_topicSubscribeExt(opaqueSession_p, flags, topicSubscription_p):
    libsolclient.solClient_session_topicSubscribeExt(opaqueSession_p, flags, topicSubscription_p)

#
# solClient_dllExport solClient_returnCode_t
#   solClient_session_topicUnsubscribeExt (solClient_opaqueSession_pt
#                                       opaqueSession_p,
#                                       solClient_subscribeFlags_t flags,
#                                       const char *topicSubscription_p);
#
def solClient_session_topicUnsubscribeExt(opaqueSession_p, flags, topicSubscription_p):
    libsolclient.solClient_session_topicUnsubscribeExt(opaqueSession_p, flags, topicSubscription_p)

#
# solClient_dllExport solClient_returnCode_t solClient_cleanup (void);
#
def solClient_cleanup():
    libsolclient.solClient_cleanup()

