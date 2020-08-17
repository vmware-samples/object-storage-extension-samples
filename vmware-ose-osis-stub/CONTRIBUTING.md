## Contributing to OSIS Implementation

### Developer Certificate of Origin

Before you start working with this project, please read our [Developer Certificate of Origin](https://cla.vmware.com/dco). All contributions to this repository must be signed as described on that page. Your signature certifies that you wrote the patch or have the right to pass it on as an open-source patch.

### What should I know before I get started?
Hand on VMware Cloud Director Object Storage Extension; and want to integrate storage platforms with OSE via OSIS.
Have overall picture of [OSE architecture](https://docs.vmware.com/en/VMware-Cloud-Director-Object-Storage-Extension/index.html). 
Also know how OSIS unifies storage platforms' administrative interfaces to integrate with OSE. 
//TODO OSIS docs  

### How Can I Contribute?
- Report/Fix bugs
- Suggest/Implement enhancement
- Add OSIS implementation for other object storage platform

#### Process of code contribution 
* Follow the [GitHub process](https://help.github.com/articles/fork-a-repo)
* Please use one branch per change-set
* Please post Cloud Director and Object Storage version, and object storage platform version for new OSIS implementation
* If you include a license with your OSIS implementation, use the project license

### Required Information
Please send a GitHub Pull Request with a clear list of what you've done.
When you send a pull request, it will be great if you include unit tests. 
Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:
```
$ git commit -m "A brief summary of the commit
> 
> A paragraph describing what changed and its impact."
```

### Code Style
[Intellij](https://www.jetbrains.com/idea/) default code style.