#! /usr/local/bin/python

#
# This module exposes part of the Solace Messaging C API to Python 2.7
#
#

from ctypes import *

libsolclient = cdll.LoadLibrary('lib/libsolclient.so.1')

#
# typedef enum solClient_log_level
# {
#   SOLCLIENT_LOG_EMERGENCY = 0, /**< This level is not used by the API. */
#   SOLCLIENT_LOG_ALERT = 1,     /**< This level is not used by the API. */
#   SOLCLIENT_LOG_CRITICAL = 2,  /**< A serious error that can make the API unusable. */
#   SOLCLIENT_LOG_ERROR = 3,     /**< An unexpected condition within the API that can affect its operation. */
#   SOLCLIENT_LOG_WARNING = 4,   /**< An unexpected condition within the API that is not expected to affect its operation. */
#   SOLCLIENT_LOG_NOTICE = 5,    /**< Significant informational messages about the normal operation of the API. These messages are never output in the normal process of sending or receiving a message from the appliance. */
#   SOLCLIENT_LOG_INFO = 6,      /**< Informational messages about the normal operation of the API. These might include information related to sending or receiving messages from the appliance. */
#   SOLCLIENT_LOG_DEBUG = 7      /**< Debugging information generally useful to API developers (very verbose). */
# } solClient_log_level_t;       /**< Type for log levels. */
#
(SOLCLIENT_LOG_EMERGENCY,
 SOLCLIENT_LOG_ALERT,
 SOLCLIENT_LOG_CRITICAL,
 SOLCLIENT_LOG_ERROR,
 SOLCLIENT_LOG_WARNING,
 SOLCLIENT_LOG_NOTICE,
 SOLCLIENT_LOG_INFO,
 SOLCLIENT_LOG_DEBUG) = map(c_int, xrange(8))
solClient_log_level_t = c_int

#
# #define SOLCLIENT_LOG_DEFAULT_FILTER (SOLCLIENT_LOG_NOTICE) /**< Default log filter level. */
#
SOLCLIENT_LOG_DEFAULT_FILTER = SOLCLIENT_LOG_NOTICE

#
# #define SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD ((solClient_propertyArray_pt )_solClient_contextPropsDefaultWithCreateThread) /**< Use with ::solClient_context_create() to create a Context in which the automatic Context thread is automatically created and all other properties are set with default values. */
#
SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD = pointer(
    c_char_p.in_dll(libsolclient, "_solClient_contextPropsDefaultWithCreateThread")
)

#
# #define SOLCLIENT_DELIVERY_MODE_DIRECT         (0x00)  /**< Send a Direct message. */
# #define SOLCLIENT_DELIVERY_MODE_PERSISTENT     (0x10)  /**< Send a Persistent message. */
# #define SOLCLIENT_DELIVERY_MODE_NONPERSISTENT  (0x20)  /**< Send a Non-Persistent message. */
#
SOLCLIENT_DELIVERY_MODE_DIRECT = c_int(0)

#
# #define SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM        (0x02) /**< The subscribe/unsubscribe call blocks until a confirmation is received. @see @ref blocking-context "Threading Effects on Blocking Modes" for more information about setting subscribe flags in the Context thread.*/
# #define SOLCLIENT_SUBSCRIBE_FLAGS_RX_ALL_DELIVER_TO_ONE (0x04) /**< This flag, when present in a subscription ADD request, overrides the deliver-to-one property in a message (see ::solClient_msg_setDeliverToOne()) - If the Topic in the message matches, it is delivered to clients with ::SOLCLIENT_SUBSCRIBE_FLAGS_RX_ALL_DELIVER_TO_ONE set, in addition to any one client that is subscribed to the Topic without this override. */
# #define SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY   (0x08) /**< For the @ref topic-dispatch "topic dispatch" feature, this flag indicates the subscription should only be added to the dispatch table and should not be added to the appliance. */
# #define SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM       (0x10) /**< Requests a confirmation for the subscribe/unsubscribe operation. This bit is implied by ::SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM. If ::SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM is not set when this flag is set, then a confirmation event will be issued through the Session event callback procedure. */
#
SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM = c_int(2)

#
# typedef void   *solClient_opaqueContext_pt;   /**< An opaque pointer to a processing Context. */
# typedef void   *solClient_opaqueSession_pt;   /**< An opaque pointer to a Session. */
# typedef void   *solClient_opaqueMsg_pt;       /**< An opaque pointer to a message. */
#
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
        ("callback_p", c_void_p),
        ("user_p", c_void_p)
    ]

# TODO (Update the types of these fields)
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
        ("callback_p", solClient_session_eventCallbackFunc_t),
        ("user_p", c_void_p)
    ]

solClient_session_rxMsgCallbackFunc_t = CFUNCTYPE(c_int, solClient_opaqueSession_pt, solClient_opaqueMsg_pt, c_void_p)
class solClient_session_createRxMsgCallbackFuncInfo_t(Structure):
    _fields_ = [
        ("callback_p", c_void_p),
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
# typedef enum solClient_destinationType
# {
#     SOLCLIENT_NULL_DESTINATION          = -1,
#     SOLCLIENT_TOPIC_DESTINATION         =  0,
#     SOLCLIENT_QUEUE_DESTINATION         =  1,
#     SOLCLIENT_TOPIC_TEMP_DESTINATION    =  2,
#     SOLCLIENT_QUEUE_TEMP_DESTINATION    =  3
# } solClient_destinationType_t;
#
# typedef struct solClient_destination 
# {
#     solClient_destinationType_t         destType; /**< The type of destination. */
#     const char *                        dest;     /**< The name of the destination (as a NULL-terminated string). */
# } solClient_destination_t;
#

(SOLCLIENT_NULL_DESTINATION,
 SOLCLIENT_TOPIC_DESTINATION,
 SOLCLIENT_QUEUE_DESTINATION,
 SOLCLIENT_TOPIC_TEMP_DESTINATION,
 SOLCLIENT_QUEUE_TEMP_DESTINATION) = map(c_int, xrange(-1, 4))
solClient_destinationType_t = c_int

class solClient_destination_t(Structure):
    _fields_ = [
        ("destType", solClient_destinationType_t),
        ("dest", c_char_p)
    ]

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
# solClient_dllExport solClient_returnCode_t
#   solClient_session_sendMsg (solClient_opaqueSession_pt opaqueSession_p,
#                           solClient_opaqueMsg_pt msg_p);
#
def solClient_session_sendMsg(opaqueSession_p, msg_p):
    libsolclient.solClient_session_sendMsg(opaqueSession_p, msg_p)

#
# solClient_dllExport solClient_returnCode_t solClient_cleanup (void);
#
def solClient_cleanup():
    libsolclient.solClient_cleanup()

