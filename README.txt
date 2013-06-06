usage: asswords.py [-h] {list,add,get,delete,push} ...

positional arguments:
  {list,add,get,delete,push}
                        Commands:
    list                List all entry names.
    add                 Add new entry.
    get                 Read a password entry. The password will be
                        temporarily written to the terminal.
    delete              Delete entry.
    push                Push changes to server. This is normally attempted
                        automatically on 'add' and 'delete', but will need to
                        be done manually if the automatic push failed (e.g. no
                        network connection).

optional arguments:
  -h, --help            show this help message and exit
