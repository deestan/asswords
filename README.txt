Tool for storing and retrieving passwords.  Backs onto a git repository.

Keeps a list of entries, where each entry consists of a "name" and a
"password".  The name is *NOT* encrypted in the storage file, while
the password is symmetrically encrypted using AES and a master passphrase.

========================================================================
                            DON'T USE THIS
========================================================================
Cryptography is hard.

Incorrectly applied cryptography is doubly evil, because in addition to
being useless, it provides a false sense of security.

While I have made an earnest effory at making this tool secure, I have
not yet done a significant analysis of the cryptography techniques
used, which makes the tool UNSAFE.
========================================================================

Before use, make sure that the directory ~/.asswords is a valid git repository, and
has a defined remote "origin".

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
