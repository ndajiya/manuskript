#!/usr/bin/env python
#--!-- coding: utf8 --!--
 
from qt import *
from enums import *
from functions import *
import re


def infoForRef(ref):
    match = re.fullmatch("::(\w):(\d+?)::", ref)
    if match:
        _type = match.group(1)
        _ref = match.group(2)
        
        if _type == "T":
            m = mainWindow().mdlOutline
            idx = m.getIndexByID(_ref)
            
            if not idx.isValid():
                return qApp.translate("references", "Unknown reference: {}.").format(ref)
            
            item = idx.internalPointer()
            
            #Titles
            pathTitle = qApp.translate("references", "Path:")
            statsTitle = qApp.translate("references", "Stats:")
            POVTitle = qApp.translate("references", "POV:")
            statusTitle = qApp.translate("references", "Status:")
            labelTitle = qApp.translate("references", "Label:")
            ssTitle = qApp.translate("references", "Short summary:")
            lsTitle = qApp.translate("references", "Long summary:")
            notesTitle = qApp.translate("references", "Notes:")
                    
            POV = ""
            if item.POV():
                POV = "<a href='{ref}'>{text}</a>".format(
                    ref="::C:{}::".format(item.POV()),
                    text=mainWindow().mdlPersos.getPersoNameByID(item.POV()))
            
            status = item.status()
            if status:
                status = mainWindow().mdlStatus.item(int(status), 0).text()
            else:
                status = ""
                
            label = item.label()
            if label:
                label = mainWindow().mdlLabels.item(int(label), 0).text()
            else:
                label = ""
            
            path = item.pathID()
            pathStr = []
            for _id, title in path:
                pathStr.append("<a href='{ref}'>{text}</a>".format(
                    ref="::T:{}::".format(_id),
                    text=title))
            path = " > ".join(pathStr)
            
            ss = item.data(Outline.summarySentance.value)
            ls = item.data(Outline.summaryFull.value)
            notes = item.data(Outline.notes.value)
            
            text = """<h1>{title}</h1>
            <p><b>{pathTitle}</b> {path}</p>
            <p><b>{statsTitle}</b> {stats}<br>
               {POV}
               {status}
               {label}</p>
            {ss}
            {ls}
            {notes}
            """.format(
                title=item.title(),
                pathTitle=pathTitle,
                path=path,
                statsTitle=statsTitle,
                stats=item.stats(),
                POV="<b>{POVTitle}</b> {POV}<br>".format(
                    POVTitle=POVTitle,
                    POV=POV) if POV else "",
                status="<b>{statusTitle}</b> {status}<br>".format(
                    statusTitle=statusTitle,
                    status=status) if status else "",
                label="<b>{labelTitle}</b> {label}</p>".format(
                    labelTitle=labelTitle,
                    label=label) if label else "",
                ss="<p><b>{ssTitle}</b> {ss}</p>".format(
                    ssTitle=ssTitle,
                    ss=ss.replace("\n", "<br>")) if ss else "",
                ls="<p><b>{lsTitle}</b><br>{ls}</p>".format(
                    lsTitle=lsTitle,
                    ls=ls.replace("\n", "<br>")) if ls else "",
                notes="<p><b>{notesTitle}</b><br>{notes}</p>".format(
                    notesTitle=notesTitle,
                    notes=linkifyAllRefs(notes).replace("\n", "<br>")) if notes else "",
                )
            
            return text
        
        elif _type == "C":
            m = mainWindow().mdlPersos
            index = m.getIndexFromID(_ref)
            name = m.name(index.row())
            
            # Titles
            basicTitle = qApp.translate("references", "Basic infos")
            detailedTitle = qApp.translate("references", "Detailed infos")
            POVof = qApp.translate("references", "POV of:")
            referencedIn = qApp.translate("references", "Referenced in:")
            
            # basic infos
            basic = []
            for i in [
                (Perso.motivation,	qApp.translate("references", "Motivation"),	False),
                (Perso.goal,	        qApp.translate("references", "Goal"),	        False),
                (Perso.conflict,	qApp.translate("references", "Conflict"),	False),
                (Perso.epiphany,	qApp.translate("references", "Epiphany"),	False),
                (Perso.summarySentance,	qApp.translate("references", "Short summary"),	True),
                (Perso.summaryPara,	qApp.translate("references", "Longer summary"),	True),
                ]:
                val = m.data(index.sibling(index.row(), i[0].value))
                if val:
                    basic .append("<b>{title}:</b>{n}{val}".format(
                        title=i[1],
                        n = "\n" if i[2] else " ",
                        val=val))
            basic = "<br>".join(basic)
            
            # detailed infos
            detailed = []
            for _name, _val in m.listPersoInfos(index):
                detailed.append("<b>{}:</b> {}".format(
                    _name,
                    _val))
            detailed = "<br>".join(detailed)
                
            # list scenes of which it is POV
            oM = mainWindow().mdlOutline
            lst = oM.findItemsByPOV(_ref)
            
            listPOV = ""
            for t in lst:
                idx = oM.getIndexByID(t)
                listPOV += "<li><a href='{link}'>{text}</a>".format(
                    link="::T:{}::".format(t),
                    text=oM.data(idx, Outline.title.value))
            
            # List scences where character is referenced
            listRefs = ""
            lst = oM.findItemsContaining(ref, Outline.notes.value)
            for t in lst:
                idx = oM.getIndexByID(t)
                listRefs += "<li><a href='{link}'>{text}</a>".format(
                    link="::T:{}::".format(t),
                    text=oM.data(idx, Outline.title.value))
            
            text = """<h1>{name}</h1>
            {basicInfos}
            {detailedInfos}
            {POV}
            {references}
            """.format(
                name=name,
                basicInfos="<h2>{basicTitle}</h2>{basic}".format(
                    basicTitle=basicTitle,
                    basic=basic) if basic else "",
                detailedInfos="<h2>{detailedTitle}</h2>{detailed}".format(
                    detailedTitle=detailedTitle,
                    detailed=detailed) if detailed else "",
                POV="<h2>{POVof}</h2><ul>{listPOV}</ul>".format(
                    POVof=POVof,
                    listPOV=listPOV) if listPOV else "",
                references="<h2>{referencedIn}</h2><ul>{listRefs}</ul>".format(
                    referencedIn=referencedIn,
                    listRefs=listRefs) if listRefs else "",
                    )
            return text
            
    else:
        return qApp.translate("references", "Unknown reference: {}.").format(ref)
    
def refToLink(ref):
    match = re.fullmatch("::(\w):(\d+?)::", ref)
    if match:
        _type = match.group(1)
        _ref = match.group(2)
        text = ""
        if _type == "T":
            m = mainWindow().mdlOutline
            idx = m.getIndexByID(_ref)
            if idx.isValid():
                item = idx.internalPointer()
                text = item.title()
            
        elif _type == "C":
            m = mainWindow().mdlPersos
            text = m.item(int(_ref), Perso.name.value).text()
            
        if text:
            return "<a href='{ref}'>{text}</a>".format(
                    ref=ref,
                    text=text)
        else:
            return ref
    
def linkifyAllRefs(text):
    return re.sub(r"::(\w):(\d+?)::", lambda m: refToLink(m.group(0)), text)
    
def tooltipForRef(ref):
    match = re.fullmatch("::(\w):(\d+?)::", ref)
    if match:
        _type = match.group(1)
        _ref = match.group(2)
        
        if _type == "T":
            m = mainWindow().mdlOutline
            idx = m.getIndexByID(_ref)
            
            if not idx.isValid():
                return qApp.translate("references", "Unknown reference: {}.").format(ref)
            
            item = idx.internalPointer()
            
            tooltip = qApp.translate("references", "Text: <b>{}</b>").format(item.title())
            tooltip += "<br><i>{}</i>".format(item.path())
            
            return tooltip
        
        elif _type == "C":
            m = mainWindow().mdlPersos
            name = m.item(int(_ref), Perso.name.value).text()
            return qApp.translate("references", "Character: <b>{}</b>").format(name)
            
    else:
        return qApp.translate("references", "Unknown reference: {}.").format(ref)
    
def openReference(ref):
    match = re.fullmatch("::(\w):(\d+?)::", ref)
    if match:
        _type = match.group(1)
        _ref = match.group(2)
        
        if _type == "C":
            mw = mainWindow()
            
            for i in range(mw.mdlPersos.rowCount()):
                if mw.mdlPersos.ID(i) == _ref:
                    mw.tabMain.setCurrentIndex(2)
                    item = mw.lstPersos.getItemByID(_ref)
                    mw.lstPersos.setCurrentItem(item)
                    return True
                
            print("Ref not found")
            return False
        
        elif _type == "T":
            
            mw = mainWindow()
            index = mw.mdlOutline.getIndexByID(_ref)
            
            if index.isValid():
                mw.mainEditor.setCurrentModelIndex(index, newTab=True)
                return True
            else:
                print("Ref not found")
                return False
        
        print("Ref not implemented")
        return False