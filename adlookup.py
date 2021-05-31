import win32com, win32com.client
import ldap

def getUserDetails(ldap_path,value_required=1):
  attrs={}
  adobj=win32com.client.GetObject(ldap_path)
  schema_obj=win32com.client.GetObject(adobj.schema)
  for i in schema_obj.MandatoryProperties:
      value=getattr(adobj,i)
      if value_required and value==None: continue
      attrs[i]=value
  for i in schema_obj.OptionalProperties:
      value=getattr(adobj,i)
      if value_required and value==None: continue
      attrs[i]=value
  return attrs
