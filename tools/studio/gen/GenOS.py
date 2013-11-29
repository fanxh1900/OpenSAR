import sys,os
import xml.etree.ElementTree as ET

__all__ = ['GenOS']

__Header = \
"""/*
* Configuration of module: Os
*
* Created by:   parai          
* Copyright:    (C)parai@foxmail.com  
*
* Configured for (MCU):    MinGW ...
*
* Module vendor:           ArcCore
* Generator version:       2.0.34
*
* Generated by easySAR Studio (https://github.com/parai/OpenSAR)
*/
"""

__dir = '.'
__root = None
def GAGet(what,which):
    """ Gen Get Attribute"""
    return what.attrib[which]
    
def GLGet(what,which=None):
    """ Gen Get List
        used to get a sub node list from what if which is None,
        else get which fron what.
    """
    global __root
    if(which == None):
        if(__root.find(what) != None):
            return __root.find(what)
        else:
            return []
    else:
        if(what.find(which) != None):
            return what.find(which)
        else:
            return []
def GenOS(wfxml):
    global __dir,__root
    __root = ET.parse(wfxml).getroot();
    __dir = os.path.dirname(wfxml)
    GenH()
    GenC()

def GenC():
    global __dir,__root
    pass
def GenH():
    global __dir,__root
    fp = open('%s/Os_Cfg.h'%(__dir),'w')
    fp.write(__Header)
    fp.write("""
#if !(((OS_SW_MAJOR_VERSION == 2) && (OS_SW_MINOR_VERSION == 0)) )
#error Os: Configuration file expected BSW module version to be 2.0.*
#endif

#ifndef OS_CFG_H_
#define OS_CFG_H_

// Application Id's
#define APPLICATION_ID_OsDefaultApplication  0  // TODO: 

// Alarm Id's
""")
    alarmid = 0
    for Alarm in GLGet('AlarmList'):
        fp.write('#define ALARM_ID_%s %s\n'%(GAGet(Alarm,'name'),alarmid))
        alarmid += 1
    fp.write('\n// Counter Id\'s\n')
    counterid = 0
    for Counter in GLGet('CounterList'):
        fp.write('#define COUNTER_ID_%s %s\n'%(GAGet(Counter,'name'),counterid))
        counterid += 1
    fp.write("""
// System counter TODO
#define OSMAXALLOWEDVALUE        UINT_MAX// NOT CONFIGURABLE IN TOOLS
#define OSTICKSPERBASE            1       // NOT CONFIGURABLE IN TOOLS
#define OSMINCYCLE                1        // NOT CONFIGURABLE IN TOOLS
#define OSTICKDURATION            1000000UL    // Time between ticks in nano seconds

// Counter macros
""")
    counterid = 0
    for Counter in GLGet('CounterList'):
        if(counterid == 0):
            max = 'OSMAXALLOWEDVALUE //TODO: I set the first counter configured by easySAR as system counter, sorry' 
        else:
            max = GAGet(Counter,'maxallowedvalue')
        fp.write('#define OSMAXALLOWEDVALUE__%s %s\n'%(GAGet(Counter,'name'),max))
        fp.write('#define OSTICKSPERBASE_%s 1 // NOT CONFIGURABLE IN TOOLS,sorry\n'%(GAGet(Counter,'name')))
        fp.write('#define OSMINCYCLE_%s %s\n'%(GAGet(Counter,'name'),GAGet(Counter,'mincycle')))
        if(counterid == 0):
            fp.write("""
#define OS_TICKS2SEC_%s(_ticks)       ( (OSTICKDURATION * _ticks)/1000000000UL )
#define OS_TICKS2MS_%s(_ticks)        ( (OSTICKDURATION * _ticks)/1000000UL )
#define OS_TICKS2US_%s(_ticks)        ( (OSTICKDURATION * _ticks)/1000UL )
#define OS_TICKS2NS_%s(_ticks)        (OSTICKDURATION * _ticks)
            """%(GAGet(Counter,'name'),GAGet(Counter,'name'),GAGet(Counter,'name'),GAGet(Counter,'name')) )
        counterid += 1
    fp.write('\n// Event masks\n')
    for Task in GLGet('TaskList'):
        for Event in GLGet(Task,'EventList'):
            fp.write('#define EVENT_MASK_%s %s // of %s\n'%(GAGet(Event,'name'),GAGet(Event,'mask'),GAGet(Task,'name')))
    fp.write("""
// Isr Id's

// Resource Id's

// Linked resource id's

// Resource masks

// Task Id's
""")  
    fp.write('#define TASK_ID_OsIdle    0 // TODO, generate it by default\n')
    taskid = 1
    for Task in GLGet('TaskList'):
        fp.write('#define TASK_ID_%s %s\n'%(GAGet(Task,'name'),taskid))
        taskid += 1
    fp.write('\n// Task entry points\n')
    fp.write('extern void OsIdle( void );\n')
    for Task in GLGet('TaskList'):
        fp.write('extern void %s( void );\n'%(GAGet(Task,'name')))
    fp.write('\n// Schedule table id\'s\n')
    fp.write("""
// Stack size
#define OS_INTERRUPT_STACK_SIZE    2048    // TODO
#define OS_OSIDLE_STACK_SIZE 512            // TODO

""")
    fp.write('#define OS_ALARM_CNT            %s\n'%(len(GLGet('AlarmList'))))
    fp.write('#define OS_TASK_CNT             %s\n'%(len(GLGet('TaskList'))))
    fp.write('#define OS_SCHTBL_CNT           %s\n'%(len(GLGet('ScheduleTableList'))))
    fp.write('#define OS_COUNTER_CNT          %s\n'%(len(GLGet('CounterList'))))
    EventCount = 0
    for Task in GLGet('TaskList'):
        for Event in GLGet(Task,'EventList'):
            EventCount += 1
    fp.write('#define OS_EVENTS_CNT           %s\n'%(EventCount))
    fp.write("""
// TODO: 
//#define OS_ISRS_CNT                 0
#define OS_RESOURCE_CNT               0
#define OS_LINKED_RESOURCE_CNT        0
#define OS_APPLICATION_CNT            1    // TODO
#define OS_SERVICE_CNT                0  /* ARCTICSTUDIO_GENERATOR_TODO */
#define CFG_OS_DEBUG                  STD_ON

#define OS_SC1                        STD_ON     /* NOT CONFIGURABLE IN TOOLS */
#define OS_USE_APPLICATIONS           STD_ON
#define OS_USE_MEMORY_PROT            STD_OFF    /* NOT CONFIGURABLE IN TOOLS */
#define OS_USE_TASK_TIMING_PROT       STD_OFF    /* NOT CONFIGURABLE IN TOOLS */
#define OS_USE_ISR_TIMING_PROT        STD_OFF    /* NOT CONFIGURABLE IN TOOLS */
//#define OS_SC3                      STD_ON     /* NOT CONFIGURABLE IN TOOLS */  
#define OS_STACK_MONITORING           STD_ON
#define OS_STATUS_EXTENDED            STD_ON
#define OS_USE_GET_SERVICE_ID         STD_ON     /* NOT CONFIGURABLE IN TOOLS */
#define OS_USE_PARAMETER_ACCESS       STD_ON     /* NOT CONFIGURABLE IN TOOLS */
#define OS_RES_SCHEDULER              STD_ON     /* NOT CONFIGURABLE IN TOOLS */

#define OS_ISR_CNT          0
#define OS_ISR2_CNT         0
#define OS_ISR1_CNT         0

#define OS_ISR_MAX_CNT      10

#define OS_NUM_CORES        1
""")
    fp.write('#endif /*OS_CFG_H_*/\n\n')
    fp.close()