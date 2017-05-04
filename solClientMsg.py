#! /usr/local/bin/python

#
# This module exposes part of the Solace Messaging C API to Python 2.7
#
#

from solClient import libsolclient

#
# solClient_dllExport solClient_returnCode_t
#   solClient_msg_alloc( solClient_opaqueMsg_pt *msg_p);
#
def solClient_msg_alloc(msg_p):
    libsolclient.solClient_msg_alloc(msg_p);

#
# solClient_dllExport solClient_returnCode_t 
#   solClient_msg_setDeliveryMode(solClient_opaqueMsg_pt msg_p,
#                                solClient_uint32_t    mode);
#
def solClient_msg_setDeliveryMode(msg_p, mode):
    libsolclient.solClient_msg_setDeliveryMode(msg_p, mode)

#
# solClient_dllExport solClient_returnCode_t 
#   solClient_msg_setDestination(solClient_opaqueMsg_pt msg_p,
#                         solClient_destination_t    *dest_p,
#                         size_t                      destSize);
#
def solClient_msg_setDestination(msg_p, dest_p, destSize):
    libsolclient.solClient_msg_setDestination(msg_p, dest_p, destSize)

#
# solClient_dllExport solClient_returnCode_t 
#   solClient_msg_setBinaryAttachment(solClient_opaqueMsg_pt msg_p,
#                              const void *                      buf_p,
#                              solClient_uint32_t                size);
#
def solClient_msg_setBinaryAttachment(msg_p, buf_p, size):
    libsolclient.solClient_msg_setBinaryAttachment(msg_p, buf_p, size)

#
# solClient_dllExport solClient_returnCode_t
#   solClient_msg_free(solClient_opaqueMsg_pt *msg_p);
#
def solClient_msg_free(msg_p):
    libsolclient.solClient_msg_free(msg_p)

