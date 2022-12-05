# P2P-Centralized Index
## Procedure to run the files
1. Open VSCode and navigate to the folder P2P-Central-Index.<br/>
2. Firstly, we have to run the server.py file.<br/>
i.  Open a new powershell terminal.<br/>
ii. Enter the below command to run the server.py file<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python server.py`
3. Secondly, we have to now the run the 1client.py file<br/>
i.  Open another new powershell terminal.<br/>
ii. Enter the below command to run the 1client.py file<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python .\1client\1client.py`
4. Next we have to now run the 2client.py file<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python .\2client\2client.py`
5. Now server will have the information about it's clients.
6. On each client terminal, 3 options (Lookup, List, Get) will be available to the user. To perform look up or list or get functions the user will have enter `1` or `2` or `3` respectively.

### Lookup Operation
If the user has selected `1`, now the user will have to enter the RFC number to search. The RFC title and the clients that have RFC will be the output

### List Operation
If the user has selected `2`, the entire RFC list along the cleints will be the output.

### Get Operation
To execute the `3`, the user will first have to do the `List Operation`. From the output of the list operation, the user should see the RFC number they want and it's respective client port number. Based on this in the client terminal the user will enter RFC to recieve and cleint port number to requst. Followed by that, the file will be available in the client folder.</br><br/>
For example, client 1 does not have RFC 1622. The user will have to enter 1622 and the client 2 port number on the client 1 powershell terminal. The file 1622 Pip Header Processing.txt will be availabe on the 1client folder now.
