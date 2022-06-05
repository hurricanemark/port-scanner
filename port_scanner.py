import socket
from common_ports import ports_and_services



#
# Function: validate_ip_address
# Determine valid IpV4 address
#
def validate_ipV4_address(address):
  parts = address.split(".")
  message = ""
  status = True
  if len(parts) != 4:
    #print("IP address {} is not valid".format(address))
    message = 'Error: Invalid IP address'
    status = False
    try:
      for part in parts:
        if not isinstance(int(part), int):
          #print("IP address {} is not valid".format(address))
          message = 'Error: Invalid IP address'
          status = False 
        if int(part) < 0 or int(part) > 255:
          message = 'Error: Invalid IP address'
          status = False
          #print("IP address {} is not valid".format(address))
    except ValueError:
      try:
        IP = socket.gethostbyname(address);
        print("Target {} is ({})".format(address, IP))
        message = "Open ports for {} ({})\n".format(address, IP)
        status = True
      except:
        message = 'Error: Invalid hostname'
        status = False
      
  print("IP address {} is valid".format(address))
  return status, message

def client_sock_connect(target, port):
  # create an INET, STREAMing socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    # now connect to the port
    # s.setblocking(False)
    s.settimeout(50.0)
    s.connect((target, port))
    s.settimeout(None)
    # s.setblocking(True)
    s.close()
    return True
  except:
    s.close()
    return False     

# 
# Function: get_open_ports()
# Usage: get_open_ports("209.216.230.240", [440, 445])
#        get_open_ports("www.stackoverflow.com", [79, 82])
# Description:
#  This function takes a target argument and a port_range argument. 
#  target can be a URL or IP address. port_range is a list of 
#  two numbers indicating the first and last numbers of the range 
#  of ports to check.
#
def get_open_ports(target, port_range, desc = False):
  open_ports = []
  
  desc_results = ""
  stat, mesg = validate_ipV4_address(target)
  
  print(stat)
  if stat == False:
    return mesg
  else:
    if desc:
      desc_results = mesg
    else:
      desc_results = "Open ports for {}\n".format(target)

  desc_results += "{}     {}".format("PORT", "SERVICE")
  
  
  
  for p in range(port_range[0], port_range[1]):
    print("Connecting {}, port {} ...".format(target, p))
    if client_sock_connect(target,p):
      # add to open_ports
      open_ports.append(p)  
      if desc:
        try:
          if ports_and_services[p] != None:
            print(p, '->', ports_and_services[p])
            desc_results += "\n{}     {}".format(target, ports_and_services[p])
        except KeyError:
          #print("Key does not exist in common_ports")
          pass
      
  if desc:
    print(">>>Desc Returing: {}\n".format(desc_results))
    return desc_results
  else:
    print(">>>NonDesc Returing: {}\n".format(open_ports))
    return open_ports
