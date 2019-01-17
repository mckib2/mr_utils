
# LOAD_DATA
## mr_utils.load_data.hdf5

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/hdf5.py)

```
NAME
    mr_utils.load_data.hdf5

FUNCTIONS
    load_hdf5(filename)


```


## mr_utils.load_data.mat

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/mat.py)

```
NAME
    mr_utils.load_data.mat

FUNCTIONS
    deal_with_7_3(data)
    
    load_mat(filename, key=None)


```


## mr_utils.load_data.npy

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/npy.py)

```
NAME
    mr_utils.load_data.npy

FUNCTIONS
    load_npy(filename)


```


## mr_utils.load_data.pyport

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/pyport.py)

```
NAME
    mr_utils.load_data.pyport

CLASSES
    builtins.object
        mdhCutOff
        mdhLC
        mdhSliceData
        mdhSlicePosVec
        sScanHeader
    
    class mdhCutOff(builtins.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class mdhLC(builtins.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class mdhSliceData(builtins.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class mdhSlicePosVec(builtins.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class sScanHeader(builtins.object)
     |  This is the VD line header
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  sizeof()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    ProcessParameterMap(doc_root, parammap_file_content)
    
    check_positive(value)
    
    get_embedded_file(file)
    
    get_ismrmrd_schema()
        Download XSD file from ISMRMD git repo.
    
    get_list_of_embedded_files()
        List of files to go try to find from the git repo.
    
    getparammap_file_content(parammap_file, usermap_file, VBFILE)
    
    main(args)
    
    readMeasurementHeaderBuffers(siemens_dat, num_buffers)
    
    readParcFileEntries(siemens_dat, ParcRaidHead, VBFILE)
        struct MrParcRaidFileEntry
        {
          uint32_t measId_;
          uint32_t fileId_;
          uint64_t off_;
          uint64_t len_;
          char patName_[64];
          char protName_[64];
        };
    
    readXmlConfig(debug_xml, parammap_file_content, num_buffers, buffers, wip_double, trajectory, dwell_time_0, max_channels, radial_views, baseLineString, protocol_name)
    
    reduce(...)
        reduce(function, sequence[, initial]) -> value
        
        Apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
        ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
        of the sequence in the calculation, and serves as a default when the
        sequence is empty.

```


## mr_utils.load_data.raw

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/raw.py)

```
NAME
    mr_utils.load_data.raw

FUNCTIONS
    load_raw(filename, use='bart', bart_args='-A', s2i_ROS=True, as_ismrmrd=False)

```


## mr_utils.load_data.siemens_to_ismrmd_client

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/siemens_to_ismrmd_client.py)

```
NAME
    mr_utils.load_data.siemens_to_ismrmd_client

CLASSES
    paramiko.transport.Transport(threading.Thread, paramiko.util.ClosingContextManager)
        FastTransport
    tqdm._tqdm.tqdm(tqdm._utils.Comparable)
        TqdmWrap
    
    class FastTransport(paramiko.transport.Transport)
     |  An SSH Transport attaches to a stream (usually a socket), negotiates an
     |  encrypted session, authenticates, and then creates stream tunnels, called
     |  `channels <.Channel>`, across the session.  Multiple channels can be
     |  multiplexed across a single session (and often are, in the case of port
     |  forwardings).
     |  
     |  Instances of this class may be used as context managers.
     |  
     |  Method resolution order:
     |      FastTransport
     |      paramiko.transport.Transport
     |      threading.Thread
     |      paramiko.util.ClosingContextManager
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, sock)
     |      Increase window size in hopes to go faster...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from paramiko.transport.Transport:
     |  
     |  __repr__(self)
     |      Returns a string representation of this object, for debugging.
     |  
     |  accept(self, timeout=None)
     |      Return the next channel opened by the client over this transport, in
     |      server mode.  If no channel is opened before the given timeout,
     |      ``None`` is returned.
     |      
     |      :param int timeout:
     |          seconds to wait for a channel, or ``None`` to wait forever
     |      :return: a new `.Channel` opened by the client
     |  
     |  add_server_key(self, key)
     |      Add a host key to the list of keys used for server mode.  When behaving
     |      as a server, the host key is used to sign certain packets during the
     |      SSH2 negotiation, so that the client can trust that we are who we say
     |      we are.  Because this is used for signing, the key must contain private
     |      key info, not just the public half.  Only one key of each type (RSA or
     |      DSS) is kept.
     |      
     |      :param .PKey key:
     |          the host key to add, usually an `.RSAKey` or `.DSSKey`.
     |  
     |  atfork(self)
     |      Terminate this Transport without closing the session.  On posix
     |      systems, if a Transport is open during process forking, both parent
     |      and child will share the underlying socket, but only one process can
     |      use the connection (without corrupting the session).  Use this method
     |      to clean up a Transport object without disrupting the other process.
     |      
     |      .. versionadded:: 1.5.3
     |  
     |  auth_gssapi_keyex(self, username)
     |      Authenticate to the server with GSS-API/SSPI if GSS-API kex is in use.
     |      
     |      :param str username: The username to authenticate as.
     |      :returns:
     |          a list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      :raises: `.BadAuthenticationType` --
     |          if GSS-API Key Exchange was not performed (and no event was passed
     |          in)
     |      :raises: `.AuthenticationException` --
     |          if the authentication failed (and no event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  auth_gssapi_with_mic(self, username, gss_host, gss_deleg_creds)
     |      Authenticate to the Server using GSS-API / SSPI.
     |      
     |      :param str username: The username to authenticate as
     |      :param str gss_host: The target host
     |      :param bool gss_deleg_creds: Delegate credentials or not
     |      :return: list of auth types permissible for the next stage of
     |               authentication (normally empty)
     |      :raises: `.BadAuthenticationType` -- if gssapi-with-mic isn't
     |          allowed by the server (and no event was passed in)
     |      :raises:
     |          `.AuthenticationException` -- if the authentication failed (and no
     |          event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  auth_interactive(self, username, handler, submethods='')
     |      Authenticate to the server interactively.  A handler is used to answer
     |      arbitrary questions from the server.  On many servers, this is just a
     |      dumb wrapper around PAM.
     |      
     |      This method will block until the authentication succeeds or fails,
     |      peroidically calling the handler asynchronously to get answers to
     |      authentication questions.  The handler may be called more than once
     |      if the server continues to ask questions.
     |      
     |      The handler is expected to be a callable that will handle calls of the
     |      form: ``handler(title, instructions, prompt_list)``.  The ``title`` is
     |      meant to be a dialog-window title, and the ``instructions`` are user
     |      instructions (both are strings).  ``prompt_list`` will be a list of
     |      prompts, each prompt being a tuple of ``(str, bool)``.  The string is
     |      the prompt and the boolean indicates whether the user text should be
     |      echoed.
     |      
     |      A sample call would thus be:
     |      ``handler('title', 'instructions', [('Password:', False)])``.
     |      
     |      The handler should return a list or tuple of answers to the server's
     |      questions.
     |      
     |      If the server requires multi-step authentication (which is very rare),
     |      this method will return a list of auth types permissible for the next
     |      step.  Otherwise, in the normal case, an empty list is returned.
     |      
     |      :param str username: the username to authenticate as
     |      :param callable handler: a handler for responding to server questions
     |      :param str submethods: a string list of desired submethods (optional)
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty).
     |      
     |      :raises: `.BadAuthenticationType` -- if public-key authentication isn't
     |          allowed by the server for this user
     |      :raises: `.AuthenticationException` -- if the authentication failed
     |      :raises: `.SSHException` -- if there was a network error
     |      
     |      .. versionadded:: 1.5
     |  
     |  auth_interactive_dumb(self, username, handler=None, submethods='')
     |      Autenticate to the server interactively but dumber.
     |      Just print the prompt and / or instructions to stdout and send back
     |      the response. This is good for situations where partial auth is
     |      achieved by key and then the user has to enter a 2fac token.
     |  
     |  auth_none(self, username)
     |      Try to authenticate to the server using no authentication at all.
     |      This will almost always fail.  It may be useful for determining the
     |      list of authentication types supported by the server, by catching the
     |      `.BadAuthenticationType` exception raised.
     |      
     |      :param str username: the username to authenticate as
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      
     |      :raises:
     |          `.BadAuthenticationType` -- if "none" authentication isn't allowed
     |          by the server for this user
     |      :raises:
     |          `.SSHException` -- if the authentication failed due to a network
     |          error
     |      
     |      .. versionadded:: 1.5
     |  
     |  auth_password(self, username, password, event=None, fallback=True)
     |      Authenticate to the server using a password.  The username and password
     |      are sent over an encrypted link.
     |      
     |      If an ``event`` is passed in, this method will return immediately, and
     |      the event will be triggered once authentication succeeds or fails.  On
     |      success, `is_authenticated` will return ``True``.  On failure, you may
     |      use `get_exception` to get more detailed error information.
     |      
     |      Since 1.1, if no event is passed, this method will block until the
     |      authentication succeeds or fails.  On failure, an exception is raised.
     |      Otherwise, the method simply returns.
     |      
     |      Since 1.5, if no event is passed and ``fallback`` is ``True`` (the
     |      default), if the server doesn't support plain password authentication
     |      but does support so-called "keyboard-interactive" mode, an attempt
     |      will be made to authenticate using this interactive mode.  If it fails,
     |      the normal exception will be thrown as if the attempt had never been
     |      made.  This is useful for some recent Gentoo and Debian distributions,
     |      which turn off plain password authentication in a misguided belief
     |      that interactive authentication is "more secure".  (It's not.)
     |      
     |      If the server requires multi-step authentication (which is very rare),
     |      this method will return a list of auth types permissible for the next
     |      step.  Otherwise, in the normal case, an empty list is returned.
     |      
     |      :param str username: the username to authenticate as
     |      :param basestring password: the password to authenticate with
     |      :param .threading.Event event:
     |          an event to trigger when the authentication attempt is complete
     |          (whether it was successful or not)
     |      :param bool fallback:
     |          ``True`` if an attempt at an automated "interactive" password auth
     |          should be made if the server doesn't support normal password auth
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      
     |      :raises:
     |          `.BadAuthenticationType` -- if password authentication isn't
     |          allowed by the server for this user (and no event was passed in)
     |      :raises:
     |          `.AuthenticationException` -- if the authentication failed (and no
     |          event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  auth_publickey(self, username, key, event=None)
     |      Authenticate to the server using a private key.  The key is used to
     |      sign data from the server, so it must include the private part.
     |      
     |      If an ``event`` is passed in, this method will return immediately, and
     |      the event will be triggered once authentication succeeds or fails.  On
     |      success, `is_authenticated` will return ``True``.  On failure, you may
     |      use `get_exception` to get more detailed error information.
     |      
     |      Since 1.1, if no event is passed, this method will block until the
     |      authentication succeeds or fails.  On failure, an exception is raised.
     |      Otherwise, the method simply returns.
     |      
     |      If the server requires multi-step authentication (which is very rare),
     |      this method will return a list of auth types permissible for the next
     |      step.  Otherwise, in the normal case, an empty list is returned.
     |      
     |      :param str username: the username to authenticate as
     |      :param .PKey key: the private key to authenticate with
     |      :param .threading.Event event:
     |          an event to trigger when the authentication attempt is complete
     |          (whether it was successful or not)
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      
     |      :raises:
     |          `.BadAuthenticationType` -- if public-key authentication isn't
     |          allowed by the server for this user (and no event was passed in)
     |      :raises:
     |          `.AuthenticationException` -- if the authentication failed (and no
     |          event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  cancel_port_forward(self, address, port)
     |      Ask the server to cancel a previous port-forwarding request.  No more
     |      connections to the given address & port will be forwarded across this
     |      ssh connection.
     |      
     |      :param str address: the address to stop forwarding
     |      :param int port: the port to stop forwarding
     |  
     |  close(self)
     |      Close this session, and any open channels that are tied to it.
     |  
     |  connect(self, hostkey=None, username='', password=None, pkey=None, gss_host=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_trust_dns=True)
     |      Negotiate an SSH2 session, and optionally verify the server's host key
     |      and authenticate using a password or private key.  This is a shortcut
     |      for `start_client`, `get_remote_server_key`, and
     |      `Transport.auth_password` or `Transport.auth_publickey`.  Use those
     |      methods if you want more control.
     |      
     |      You can use this method immediately after creating a Transport to
     |      negotiate encryption with a server.  If it fails, an exception will be
     |      thrown.  On success, the method will return cleanly, and an encrypted
     |      session exists.  You may immediately call `open_channel` or
     |      `open_session` to get a `.Channel` object, which is used for data
     |      transfer.
     |      
     |      .. note::
     |          If you fail to supply a password or private key, this method may
     |          succeed, but a subsequent `open_channel` or `open_session` call may
     |          fail because you haven't authenticated yet.
     |      
     |      :param .PKey hostkey:
     |          the host key expected from the server, or ``None`` if you don't
     |          want to do host key verification.
     |      :param str username: the username to authenticate as.
     |      :param str password:
     |          a password to use for authentication, if you want to use password
     |          authentication; otherwise ``None``.
     |      :param .PKey pkey:
     |          a private key to use for authentication, if you want to use private
     |          key authentication; otherwise ``None``.
     |      :param str gss_host:
     |          The target's name in the kerberos database. Default: hostname
     |      :param bool gss_auth:
     |          ``True`` if you want to use GSS-API authentication.
     |      :param bool gss_kex:
     |          Perform GSS-API Key Exchange and user authentication.
     |      :param bool gss_deleg_creds:
     |          Whether to delegate GSS-API client credentials.
     |      :param gss_trust_dns:
     |          Indicates whether or not the DNS is trusted to securely
     |          canonicalize the name of the host being connected to (default
     |          ``True``).
     |      
     |      :raises: `.SSHException` -- if the SSH2 negotiation fails, the host key
     |          supplied by the server is incorrect, or authentication fails.
     |      
     |      .. versionchanged:: 2.3
     |          Added the ``gss_trust_dns`` argument.
     |  
     |  get_banner(self)
     |      Return the banner supplied by the server upon connect. If no banner is
     |      supplied, this method returns ``None``.
     |      
     |      :returns: server supplied banner (`str`), or ``None``.
     |      
     |      .. versionadded:: 1.13
     |  
     |  get_exception(self)
     |      Return any exception that happened during the last server request.
     |      This can be used to fetch more specific error information after using
     |      calls like `start_client`.  The exception (if any) is cleared after
     |      this call.
     |      
     |      :return:
     |          an exception, or ``None`` if there is no stored exception.
     |      
     |      .. versionadded:: 1.1
     |  
     |  get_hexdump(self)
     |      Return ``True`` if the transport is currently logging hex dumps of
     |      protocol traffic.
     |      
     |      :return: ``True`` if hex dumps are being logged, else ``False``.
     |      
     |      .. versionadded:: 1.4
     |  
     |  get_log_channel(self)
     |      Return the channel name used for this transport's logging.
     |      
     |      :return: channel name as a `str`
     |      
     |      .. versionadded:: 1.2
     |  
     |  get_remote_server_key(self)
     |      Return the host key of the server (in client mode).
     |      
     |      .. note::
     |          Previously this call returned a tuple of ``(key type, key
     |          string)``. You can get the same effect by calling `.PKey.get_name`
     |          for the key type, and ``str(key)`` for the key string.
     |      
     |      :raises: `.SSHException` -- if no session is currently active.
     |      
     |      :return: public key (`.PKey`) of the remote server
     |  
     |  get_security_options(self)
     |      Return a `.SecurityOptions` object which can be used to tweak the
     |      encryption algorithms this transport will permit (for encryption,
     |      digest/hash operations, public keys, and key exchanges) and the order
     |      of preference for them.
     |  
     |  get_server_key(self)
     |      Return the active host key, in server mode.  After negotiating with the
     |      client, this method will return the negotiated host key.  If only one
     |      type of host key was set with `add_server_key`, that's the only key
     |      that will ever be returned.  But in cases where you have set more than
     |      one type of host key (for example, an RSA key and a DSS key), the key
     |      type will be negotiated by the client, and this method will return the
     |      key of the type agreed on.  If the host key has not been negotiated
     |      yet, ``None`` is returned.  In client mode, the behavior is undefined.
     |      
     |      :return:
     |          host key (`.PKey`) of the type negotiated by the client, or
     |          ``None``.
     |  
     |  get_username(self)
     |      Return the username this connection is authenticated for.  If the
     |      session is not authenticated (or authentication failed), this method
     |      returns ``None``.
     |      
     |      :return: username that was authenticated (a `str`), or ``None``.
     |  
     |  getpeername(self)
     |      Return the address of the remote side of this Transport, if possible.
     |      
     |      This is effectively a wrapper around ``getpeername`` on the underlying
     |      socket.  If the socket-like object has no ``getpeername`` method, then
     |      ``("unknown", 0)`` is returned.
     |      
     |      :return:
     |          the address of the remote host, if known, as a ``(str, int)``
     |          tuple.
     |  
     |  global_request(self, kind, data=None, wait=True)
     |      Make a global request to the remote host.  These are normally
     |      extensions to the SSH2 protocol.
     |      
     |      :param str kind: name of the request.
     |      :param tuple data:
     |          an optional tuple containing additional data to attach to the
     |          request.
     |      :param bool wait:
     |          ``True`` if this method should not return until a response is
     |          received; ``False`` otherwise.
     |      :return:
     |          a `.Message` containing possible additional data if the request was
     |          successful (or an empty `.Message` if ``wait`` was ``False``);
     |          ``None`` if the request was denied.
     |  
     |  is_active(self)
     |      Return true if this session is active (open).
     |      
     |      :return:
     |          True if the session is still active (open); False if the session is
     |          closed
     |  
     |  is_authenticated(self)
     |      Return true if this session is active and authenticated.
     |      
     |      :return:
     |          True if the session is still open and has been authenticated
     |          successfully; False if authentication failed and/or the session is
     |          closed.
     |  
     |  open_channel(self, kind, dest_addr=None, src_addr=None, window_size=None, max_packet_size=None, timeout=None)
     |      Request a new channel to the server. `Channels <.Channel>` are
     |      socket-like objects used for the actual transfer of data across the
     |      session. You may only request a channel after negotiating encryption
     |      (using `connect` or `start_client`) and authenticating.
     |      
     |      .. note:: Modifying the the window and packet sizes might have adverse
     |          effects on the channel created. The default values are the same
     |          as in the OpenSSH code base and have been battle tested.
     |      
     |      :param str kind:
     |          the kind of channel requested (usually ``"session"``,
     |          ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``)
     |      :param tuple dest_addr:
     |          the destination address (address + port tuple) of this port
     |          forwarding, if ``kind`` is ``"forwarded-tcpip"`` or
     |          ``"direct-tcpip"`` (ignored for other channel types)
     |      :param src_addr: the source address of this port forwarding, if
     |          ``kind`` is ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``
     |      :param int window_size:
     |          optional window size for this session.
     |      :param int max_packet_size:
     |          optional max packet size for this session.
     |      :param float timeout:
     |          optional timeout opening a channel, default 3600s (1h)
     |      
     |      :return: a new `.Channel` on success
     |      
     |      :raises:
     |          `.SSHException` -- if the request is rejected, the session ends
     |          prematurely or there is a timeout openning a channel
     |      
     |      .. versionchanged:: 1.15
     |          Added the ``window_size`` and ``max_packet_size`` arguments.
     |  
     |  open_forward_agent_channel(self)
     |      Request a new channel to the client, of type
     |      ``"auth-agent@openssh.com"``.
     |      
     |      This is just an alias for ``open_channel('auth-agent@openssh.com')``.
     |      
     |      :return: a new `.Channel`
     |      
     |      :raises: `.SSHException` --
     |          if the request is rejected or the session ends prematurely
     |  
     |  open_forwarded_tcpip_channel(self, src_addr, dest_addr)
     |      Request a new channel back to the client, of type ``forwarded-tcpip``.
     |      
     |      This is used after a client has requested port forwarding, for sending
     |      incoming connections back to the client.
     |      
     |      :param src_addr: originator's address
     |      :param dest_addr: local (server) connected address
     |  
     |  open_session(self, window_size=None, max_packet_size=None, timeout=None)
     |      Request a new channel to the server, of type ``"session"``.  This is
     |      just an alias for calling `open_channel` with an argument of
     |      ``"session"``.
     |      
     |      .. note:: Modifying the the window and packet sizes might have adverse
     |          effects on the session created. The default values are the same
     |          as in the OpenSSH code base and have been battle tested.
     |      
     |      :param int window_size:
     |          optional window size for this session.
     |      :param int max_packet_size:
     |          optional max packet size for this session.
     |      
     |      :return: a new `.Channel`
     |      
     |      :raises:
     |          `.SSHException` -- if the request is rejected or the session ends
     |          prematurely
     |      
     |      .. versionchanged:: 1.13.4/1.14.3/1.15.3
     |          Added the ``timeout`` argument.
     |      .. versionchanged:: 1.15
     |          Added the ``window_size`` and ``max_packet_size`` arguments.
     |  
     |  open_sftp_client(self)
     |      Create an SFTP client channel from an open transport.  On success, an
     |      SFTP session will be opened with the remote host, and a new
     |      `.SFTPClient` object will be returned.
     |      
     |      :return:
     |          a new `.SFTPClient` referring to an sftp session (channel) across
     |          this transport
     |  
     |  open_x11_channel(self, src_addr=None)
     |      Request a new channel to the client, of type ``"x11"``.  This
     |      is just an alias for ``open_channel('x11', src_addr=src_addr)``.
     |      
     |      :param tuple src_addr:
     |          the source address (``(str, int)``) of the x11 server (port is the
     |          x11 port, ie. 6010)
     |      :return: a new `.Channel`
     |      
     |      :raises:
     |          `.SSHException` -- if the request is rejected or the session ends
     |          prematurely
     |  
     |  renegotiate_keys(self)
     |      Force this session to switch to new keys.  Normally this is done
     |      automatically after the session hits a certain number of packets or
     |      bytes sent or received, but this method gives you the option of forcing
     |      new keys whenever you want.  Negotiating new keys causes a pause in
     |      traffic both ways as the two sides swap keys and do computations.  This
     |      method returns when the session has switched to new keys.
     |      
     |      :raises:
     |          `.SSHException` -- if the key renegotiation failed (which causes
     |          the session to end)
     |  
     |  request_port_forward(self, address, port, handler=None)
     |      Ask the server to forward TCP connections from a listening port on
     |      the server, across this SSH session.
     |      
     |      If a handler is given, that handler is called from a different thread
     |      whenever a forwarded connection arrives.  The handler parameters are::
     |      
     |          handler(
     |              channel,
     |              (origin_addr, origin_port),
     |              (server_addr, server_port),
     |          )
     |      
     |      where ``server_addr`` and ``server_port`` are the address and port that
     |      the server was listening on.
     |      
     |      If no handler is set, the default behavior is to send new incoming
     |      forwarded connections into the accept queue, to be picked up via
     |      `accept`.
     |      
     |      :param str address: the address to bind when forwarding
     |      :param int port:
     |          the port to forward, or 0 to ask the server to allocate any port
     |      :param callable handler:
     |          optional handler for incoming forwarded connections, of the form
     |          ``func(Channel, (str, int), (str, int))``.
     |      
     |      :return: the port number (`int`) allocated by the server
     |      
     |      :raises:
     |          `.SSHException` -- if the server refused the TCP forward request
     |  
     |  run(self)
     |      Method representing the thread's activity.
     |      
     |      You may override this method in a subclass. The standard run() method
     |      invokes the callable object passed to the object's constructor as the
     |      target argument, if any, with sequential and keyword arguments taken
     |      from the args and kwargs arguments, respectively.
     |  
     |  send_ignore(self, byte_count=None)
     |      Send a junk packet across the encrypted link.  This is sometimes used
     |      to add "noise" to a connection to confuse would-be attackers.  It can
     |      also be used as a keep-alive for long lived connections traversing
     |      firewalls.
     |      
     |      :param int byte_count:
     |          the number of random bytes to send in the payload of the ignored
     |          packet -- defaults to a random number from 10 to 41.
     |  
     |  set_gss_host(self, gss_host, trust_dns=True, gssapi_requested=True)
     |      Normalize/canonicalize ``self.gss_host`` depending on various factors.
     |      
     |      :param str gss_host:
     |          The explicitly requested GSS-oriented hostname to connect to (i.e.
     |          what the host's name is in the Kerberos database.) Defaults to
     |          ``self.hostname`` (which will be the 'real' target hostname and/or
     |          host portion of given socket object.)
     |      :param bool trust_dns:
     |          Indicates whether or not DNS is trusted; if true, DNS will be used
     |          to canonicalize the GSS hostname (which again will either be
     |          ``gss_host`` or the transport's default hostname.)
     |          (Defaults to True due to backwards compatibility.)
     |      :param bool gssapi_requested:
     |          Whether GSSAPI key exchange or authentication was even requested.
     |          If not, this is a no-op and nothing happens
     |          (and ``self.gss_host`` is not set.)
     |          (Defaults to True due to backwards compatibility.)
     |      :returns: ``None``.
     |  
     |  set_hexdump(self, hexdump)
     |      Turn on/off logging a hex dump of protocol traffic at DEBUG level in
     |      the logs.  Normally you would want this off (which is the default),
     |      but if you are debugging something, it may be useful.
     |      
     |      :param bool hexdump:
     |          ``True`` to log protocol traffix (in hex) to the log; ``False``
     |          otherwise.
     |  
     |  set_keepalive(self, interval)
     |      Turn on/off keepalive packets (default is off).  If this is set, after
     |      ``interval`` seconds without sending any data over the connection, a
     |      "keepalive" packet will be sent (and ignored by the remote host).  This
     |      can be useful to keep connections alive over a NAT, for example.
     |      
     |      :param int interval:
     |          seconds to wait before sending a keepalive packet (or
     |          0 to disable keepalives).
     |  
     |  set_log_channel(self, name)
     |      Set the channel for this transport's logging.  The default is
     |      ``"paramiko.transport"`` but it can be set to anything you want. (See
     |      the `.logging` module for more info.)  SSH Channels will log to a
     |      sub-channel of the one specified.
     |      
     |      :param str name: new channel name for logging
     |      
     |      .. versionadded:: 1.1
     |  
     |  set_subsystem_handler(self, name, handler, *larg, **kwarg)
     |      Set the handler class for a subsystem in server mode.  If a request
     |      for this subsystem is made on an open ssh channel later, this handler
     |      will be constructed and called -- see `.SubsystemHandler` for more
     |      detailed documentation.
     |      
     |      Any extra parameters (including keyword arguments) are saved and
     |      passed to the `.SubsystemHandler` constructor later.
     |      
     |      :param str name: name of the subsystem.
     |      :param handler:
     |          subclass of `.SubsystemHandler` that handles this subsystem.
     |  
     |  start_client(self, event=None, timeout=None)
     |      Negotiate a new SSH2 session as a client.  This is the first step after
     |      creating a new `.Transport`.  A separate thread is created for protocol
     |      negotiation.
     |      
     |      If an event is passed in, this method returns immediately.  When
     |      negotiation is done (successful or not), the given ``Event`` will
     |      be triggered.  On failure, `is_active` will return ``False``.
     |      
     |      (Since 1.4) If ``event`` is ``None``, this method will not return until
     |      negotiation is done.  On success, the method returns normally.
     |      Otherwise an SSHException is raised.
     |      
     |      After a successful negotiation, you will usually want to authenticate,
     |      calling `auth_password <Transport.auth_password>` or
     |      `auth_publickey <Transport.auth_publickey>`.
     |      
     |      .. note:: `connect` is a simpler method for connecting as a client.
     |      
     |      .. note::
     |          After calling this method (or `start_server` or `connect`), you
     |          should no longer directly read from or write to the original socket
     |          object.
     |      
     |      :param .threading.Event event:
     |          an event to trigger when negotiation is complete (optional)
     |      
     |      :param float timeout:
     |          a timeout, in seconds, for SSH2 session negotiation (optional)
     |      
     |      :raises:
     |          `.SSHException` -- if negotiation fails (and no ``event`` was
     |          passed in)
     |  
     |  start_server(self, event=None, server=None)
     |      Negotiate a new SSH2 session as a server.  This is the first step after
     |      creating a new `.Transport` and setting up your server host key(s).  A
     |      separate thread is created for protocol negotiation.
     |      
     |      If an event is passed in, this method returns immediately.  When
     |      negotiation is done (successful or not), the given ``Event`` will
     |      be triggered.  On failure, `is_active` will return ``False``.
     |      
     |      (Since 1.4) If ``event`` is ``None``, this method will not return until
     |      negotiation is done.  On success, the method returns normally.
     |      Otherwise an SSHException is raised.
     |      
     |      After a successful negotiation, the client will need to authenticate.
     |      Override the methods `get_allowed_auths
     |      <.ServerInterface.get_allowed_auths>`, `check_auth_none
     |      <.ServerInterface.check_auth_none>`, `check_auth_password
     |      <.ServerInterface.check_auth_password>`, and `check_auth_publickey
     |      <.ServerInterface.check_auth_publickey>` in the given ``server`` object
     |      to control the authentication process.
     |      
     |      After a successful authentication, the client should request to open a
     |      channel.  Override `check_channel_request
     |      <.ServerInterface.check_channel_request>` in the given ``server``
     |      object to allow channels to be opened.
     |      
     |      .. note::
     |          After calling this method (or `start_client` or `connect`), you
     |          should no longer directly read from or write to the original socket
     |          object.
     |      
     |      :param .threading.Event event:
     |          an event to trigger when negotiation is complete.
     |      :param .ServerInterface server:
     |          an object used to perform authentication and create `channels
     |          <.Channel>`
     |      
     |      :raises:
     |          `.SSHException` -- if negotiation fails (and no ``event`` was
     |          passed in)
     |  
     |  stop_thread(self)
     |  
     |  use_compression(self, compress=True)
     |      Turn on/off compression.  This will only have an affect before starting
     |      the transport (ie before calling `connect`, etc).  By default,
     |      compression is off since it negatively affects interactive sessions.
     |      
     |      :param bool compress:
     |          ``True`` to ask the remote client/server to compress traffic;
     |          ``False`` to refuse compression
     |      
     |      .. versionadded:: 1.5.2
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from paramiko.transport.Transport:
     |  
     |  load_server_moduli(filename=None)
     |      (optional)
     |      Load a file of prime moduli for use in doing group-exchange key
     |      negotiation in server mode.  It's a rather obscure option and can be
     |      safely ignored.
     |      
     |      In server mode, the remote client may request "group-exchange" key
     |      negotiation, which asks the server to send a random prime number that
     |      fits certain criteria.  These primes are pretty difficult to compute,
     |      so they can't be generated on demand.  But many systems contain a file
     |      of suitable primes (usually named something like ``/etc/ssh/moduli``).
     |      If you call `load_server_moduli` and it returns ``True``, then this
     |      file of primes has been loaded and we will support "group-exchange" in
     |      server mode.  Otherwise server mode will just claim that it doesn't
     |      support that method of key negotiation.
     |      
     |      :param str filename:
     |          optional path to the moduli file, if you happen to know that it's
     |          not in a standard location.
     |      :return:
     |          True if a moduli file was successfully loaded; False otherwise.
     |      
     |      .. note:: This has no effect when used in client mode.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from threading.Thread:
     |  
     |  getName(self)
     |  
     |  isAlive = is_alive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  isDaemon(self)
     |  
     |  is_alive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  join(self, timeout=None)
     |      Wait until the thread terminates.
     |      
     |      This blocks the calling thread until the thread whose join() method is
     |      called terminates -- either normally or through an unhandled exception
     |      or until the optional timeout occurs.
     |      
     |      When the timeout argument is present and not None, it should be a
     |      floating point number specifying a timeout for the operation in seconds
     |      (or fractions thereof). As join() always returns None, you must call
     |      isAlive() after join() to decide whether a timeout happened -- if the
     |      thread is still alive, the join() call timed out.
     |      
     |      When the timeout argument is not present or None, the operation will
     |      block until the thread terminates.
     |      
     |      A thread can be join()ed many times.
     |      
     |      join() raises a RuntimeError if an attempt is made to join the current
     |      thread as that would cause a deadlock. It is also an error to join() a
     |      thread before it has been started and attempts to do so raises the same
     |      exception.
     |  
     |  setDaemon(self, daemonic)
     |  
     |  setName(self, name)
     |  
     |  start(self)
     |      Start the thread's activity.
     |      
     |      It must be called at most once per thread object. It arranges for the
     |      object's run() method to be invoked in a separate thread of control.
     |      
     |      This method will raise a RuntimeError if called more than once on the
     |      same thread object.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from threading.Thread:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  daemon
     |      A boolean value indicating whether this thread is a daemon thread.
     |      
     |      This must be set before start() is called, otherwise RuntimeError is
     |      raised. Its initial value is inherited from the creating thread; the
     |      main thread is not a daemon thread and therefore all threads created in
     |      the main thread default to daemon = False.
     |      
     |      The entire Python program exits when no alive non-daemon threads are
     |      left.
     |  
     |  ident
     |      Thread identifier of this thread or None if it has not been started.
     |      
     |      This is a nonzero integer. See the get_ident() function. Thread
     |      identifiers may be recycled when a thread exits and another thread is
     |      created. The identifier is available even after the thread has exited.
     |  
     |  name
     |      A string used for identification purposes only.
     |      
     |      It has no semantics. Multiple threads may be given the same name. The
     |      initial name is set by the constructor.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from paramiko.util.ClosingContextManager:
     |  
     |  __enter__(self)
     |  
     |  __exit__(self, type, value, traceback)
    
    class TqdmWrap(tqdm._tqdm.tqdm)
     |  Decorate an iterable object, returning an iterator which acts exactly
     |  like the original iterable, but prints a dynamically updating
     |  progressbar every time a value is requested.
     |  
     |  Method resolution order:
     |      TqdmWrap
     |      tqdm._tqdm.tqdm
     |      tqdm._utils.Comparable
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  viewBar(self, a, b)
     |      Monitor progress of sftp transfers
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from tqdm._tqdm.tqdm:
     |  
     |  __del__(self)
     |  
     |  __enter__(self)
     |  
     |  __exit__(self, *exc)
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, iterable=None, desc=None, total=None, leave=True, file=None, ncols=None, mininterval=0.1, maxinterval=10.0, miniters=None, ascii=None, disable=False, unit='it', unit_scale=False, dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0, position=None, postfix=None, unit_divisor=1000, gui=False, **kwargs)
     |      Parameters
     |      ----------
     |      iterable  : iterable, optional
     |          Iterable to decorate with a progressbar.
     |          Leave blank to manually manage the updates.
     |      desc  : str, optional
     |          Prefix for the progressbar.
     |      total  : int, optional
     |          The number of expected iterations. If unspecified,
     |          len(iterable) is used if possible. As a last resort, only basic
     |          progress statistics are displayed (no ETA, no progressbar).
     |          If `gui` is True and this parameter needs subsequent updating,
     |          specify an initial arbitrary large positive integer,
     |          e.g. int(9e9).
     |      leave  : bool, optional
     |          If [default: True], keeps all traces of the progressbar
     |          upon termination of iteration.
     |      file  : `io.TextIOWrapper` or `io.StringIO`, optional
     |          Specifies where to output the progress messages
     |          (default: sys.stderr). Uses `file.write(str)` and `file.flush()`
     |          methods.
     |      ncols  : int, optional
     |          The width of the entire output message. If specified,
     |          dynamically resizes the progressbar to stay within this bound.
     |          If unspecified, attempts to use environment width. The
     |          fallback is a meter width of 10 and no limit for the counter and
     |          statistics. If 0, will not print any meter (only stats).
     |      mininterval  : float, optional
     |          Minimum progress display update interval [default: 0.1] seconds.
     |      maxinterval  : float, optional
     |          Maximum progress display update interval [default: 10] seconds.
     |          Automatically adjusts `miniters` to correspond to `mininterval`
     |          after long display update lag. Only works if `dynamic_miniters`
     |          or monitor thread is enabled.
     |      miniters  : int, optional
     |          Minimum progress display update interval, in iterations.
     |          If 0 and `dynamic_miniters`, will automatically adjust to equal
     |          `mininterval` (more CPU efficient, good for tight loops).
     |          If > 0, will skip display of specified number of iterations.
     |          Tweak this and `mininterval` to get very efficient loops.
     |          If your progress is erratic with both fast and slow iterations
     |          (network, skipping items, etc) you should set miniters=1.
     |      ascii  : bool, optional
     |          If unspecified or False, use unicode (smooth blocks) to fill
     |          the meter. The fallback is to use ASCII characters `1-9 #`.
     |      disable  : bool, optional
     |          Whether to disable the entire progressbar wrapper
     |          [default: False]. If set to None, disable on non-TTY.
     |      unit  : str, optional
     |          String that will be used to define the unit of each iteration
     |          [default: it].
     |      unit_scale  : bool or int or float, optional
     |          If 1 or True, the number of iterations will be reduced/scaled
     |          automatically and a metric prefix following the
     |          International System of Units standard will be added
     |          (kilo, mega, etc.) [default: False]. If any other non-zero
     |          number, will scale `total` and `n`.
     |      dynamic_ncols  : bool, optional
     |          If set, constantly alters `ncols` to the environment (allowing
     |          for window resizes) [default: False].
     |      smoothing  : float, optional
     |          Exponential moving average smoothing factor for speed estimates
     |          (ignored in GUI mode). Ranges from 0 (average speed) to 1
     |          (current/instantaneous speed) [default: 0.3].
     |      bar_format  : str, optional
     |          Specify a custom bar string formatting. May impact performance.
     |          [default: '{l_bar}{bar}{r_bar}'], where
     |          l_bar='{desc}: {percentage:3.0f}%|' and
     |          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
     |            '{rate_fmt}{postfix}]'
     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.
     |          Note that a trailing ": " is automatically removed after {desc}
     |          if the latter is empty.
     |      initial  : int, optional
     |          The initial counter value. Useful when restarting a progress
     |          bar [default: 0].
     |      position  : int, optional
     |          Specify the line offset to print this bar (starting from 0)
     |          Automatic if unspecified.
     |          Useful to manage multiple bars at once (eg, from threads).
     |      postfix  : dict or *, optional
     |          Specify additional stats to display at the end of the bar.
     |          Calls `set_postfix(**postfix)` if possible (dict).
     |      unit_divisor  : float, optional
     |          [default: 1000], ignored unless `unit_scale` is True.
     |      gui  : bool, optional
     |          WARNING: internal parameter - do not use.
     |          Use tqdm_gui(...) instead. If set, will attempt to use
     |          matplotlib animations for a graphical output [default: False].
     |      
     |      Returns
     |      -------
     |      out  : decorated iterator.
     |  
     |  __iter__(self)
     |      Backward-compatibility to use: for x in tqdm(iterable)
     |  
     |  __len__(self)
     |  
     |  __repr__(self, elapsed=None)
     |      Return repr(self).
     |  
     |  clear(self, nolock=False)
     |      Clear current bar display
     |  
     |  close(self)
     |      Cleanup and (if leave=False) close the progressbar.
     |  
     |  moveto(self, n)
     |  
     |  refresh(self, nolock=False)
     |      Force refresh the display of this bar
     |  
     |  set_description(self, desc=None, refresh=True)
     |      Set/modify description of the progress bar.
     |      
     |      Parameters
     |      ----------
     |      desc  : str, optional
     |      refresh  : bool, optional
     |          Forces refresh [default: True].
     |  
     |  set_description_str(self, desc=None, refresh=True)
     |      Set/modify description without ': ' appended.
     |  
     |  set_postfix(self, ordered_dict=None, refresh=True, **kwargs)
     |      Set/modify postfix (additional stats)
     |      with automatic formatting based on datatype.
     |      
     |      Parameters
     |      ----------
     |      ordered_dict  : dict or OrderedDict, optional
     |      refresh  : bool, optional
     |          Forces refresh [default: True].
     |      kwargs  : dict, optional
     |  
     |  set_postfix_str(self, s='', refresh=True)
     |      Postfix without dictionary expansion, similar to prefix handling.
     |  
     |  unpause(self)
     |      Restart tqdm timer from last print time.
     |  
     |  update(self, n=1)
     |      Manually update the progress bar, useful for streams
     |      such as reading files.
     |      E.g.:
     |      >>> t = tqdm(total=filesize) # Initialise
     |      >>> for current_buffer in stream:
     |      ...    ...
     |      ...    t.update(len(current_buffer))
     |      >>> t.close()
     |      The last line is highly recommended, but possibly not necessary if
     |      `t.update()` will be called in such a way that `filesize` will be
     |      exactly reached and printed.
     |      
     |      Parameters
     |      ----------
     |      n  : int, optional
     |          Increment to add to the internal counter of iterations
     |          [default: 1].
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from tqdm._tqdm.tqdm:
     |  
     |  external_write_mode(file=None, nolock=False) from builtins.type
     |      Disable tqdm within context and refresh tqdm when exits.
     |      Useful when writing to standard output stream
     |  
     |  get_lock() from builtins.type
     |  
     |  pandas(*targs, **tkwargs) from builtins.type
     |      Registers the given `tqdm` class with
     |          pandas.core.
     |          ( frame.DataFrame
     |          | series.Series
     |          | groupby.DataFrameGroupBy
     |          | groupby.SeriesGroupBy
     |          ).progress_apply
     |      
     |      A new instance will be create every time `progress_apply` is called,
     |      and each instance will automatically close() upon completion.
     |      
     |      Parameters
     |      ----------
     |      targs, tkwargs  : arguments for the tqdm instance
     |      
     |      Examples
     |      --------
     |      >>> import pandas as pd
     |      >>> import numpy as np
     |      >>> from tqdm import tqdm, tqdm_gui
     |      >>>
     |      >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
     |      >>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs, etc
     |      >>> # Now you can use `progress_apply` instead of `apply`
     |      >>> df.groupby(0).progress_apply(lambda x: x**2)
     |      
     |      References
     |      ----------
     |      https://stackoverflow.com/questions/18603270/
     |      progress-indicator-during-pandas-operations-python
     |  
     |  set_lock(lock) from builtins.type
     |  
     |  write(s, file=None, end='\n', nolock=False) from builtins.type
     |      Print a message via tqdm (without overlap with bars)
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from tqdm._tqdm.tqdm:
     |  
     |  __new__(cls, *args, **kwargs)
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ema(x, mu=None, alpha=0.3)
     |              Exponential moving average: smoothing to give progressively lower
     |              weights to older values.
     |      
     |      Parameters
     |      ----------
     |      x  : float
     |          New value to include in EMA.
     |      mu  : float, optional
     |          Previous EMA value.
     |      alpha  : float, optional
     |          Smoothing factor in range [0, 1], [default: 0.3].
     |          Increase to give more weight to recent values.
     |                      Ranges from 0 (yields mu) to 1 (yields x).
     |  
     |  format_interval(t)
     |      Formats a number of seconds as a clock time, [H:]MM:SS
     |      
     |      Parameters
     |      ----------
     |      t  : int
     |          Number of seconds.
     |      
     |      Returns
     |      -------
     |      out  : str
     |          [H:]MM:SS
     |  
     |  format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False, unit='it', unit_scale=False, rate=None, bar_format=None, postfix=None, unit_divisor=1000)
     |      Return a string-based progress bar given some parameters
     |      
     |      Parameters
     |      ----------
     |      n  : int
     |          Number of finished iterations.
     |      total  : int
     |          The expected total number of iterations. If meaningless (), only
     |          basic progress statistics are displayed (no ETA).
     |      elapsed  : float
     |          Number of seconds passed since start.
     |      ncols  : int, optional
     |          The width of the entire output message. If specified,
     |          dynamically resizes the progress meter to stay within this bound
     |          [default: None]. The fallback meter width is 10 for the progress
     |          bar + no limit for the iterations counter and statistics. If 0,
     |          will not print any meter (only stats).
     |      prefix  : str, optional
     |          Prefix message (included in total width) [default: ''].
     |          Use as {desc} in bar_format string.
     |      ascii  : bool, optional
     |          If not set, use unicode (smooth blocks) to fill the meter
     |          [default: False]. The fallback is to use ASCII characters
     |          (1-9 #).
     |      unit  : str, optional
     |          The iteration unit [default: 'it'].
     |      unit_scale  : bool or int or float, optional
     |          If 1 or True, the number of iterations will be printed with an
     |          appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)
     |          [default: False]. If any other non-zero number, will scale
     |          `total` and `n`.
     |      rate  : float, optional
     |          Manual override for iteration rate.
     |          If [default: None], uses n/elapsed.
     |      bar_format  : str, optional
     |          Specify a custom bar string formatting. May impact performance.
     |          [default: '{l_bar}{bar}{r_bar}'], where
     |          l_bar='{desc}: {percentage:3.0f}%|' and
     |          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
     |            '{rate_fmt}{postfix}]'
     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.
     |          Note that a trailing ": " is automatically removed after {desc}
     |          if the latter is empty.
     |      postfix  : *, optional
     |          Similar to `prefix`, but placed at the end
     |          (e.g. for additional stats).
     |          Note: postfix is usually a string (not a dict) for this method,
     |          and will if possible be set to postfix = ', ' + postfix.
     |          However other types are supported (#382).
     |      unit_divisor  : float, optional
     |          [default: 1000], ignored unless `unit_scale` is True.
     |      
     |      Returns
     |      -------
     |      out  : Formatted meter and stats, ready to display.
     |  
     |  format_num(n)
     |      Intelligent scientific notation (.3g).
     |      
     |      Parameters
     |      ----------
     |      n  : int or float or Numeric
     |          A Number.
     |      
     |      Returns
     |      -------
     |      out  : str
     |          Formatted number.
     |  
     |  format_sizeof(num, suffix='', divisor=1000)
     |      Formats a number (greater than unity) with SI Order of Magnitude
     |      prefixes.
     |      
     |      Parameters
     |      ----------
     |      num  : float
     |          Number ( >= 1) to format.
     |      suffix  : str, optional
     |          Post-postfix [default: ''].
     |      divisor  : float, optionl
     |          Divisor between prefixes [default: 1000].
     |      
     |      Returns
     |      -------
     |      out  : str
     |          Number with Order of Magnitude SI unit postfix.
     |  
     |  status_printer(file)
     |      Manage the printing and in-place updating of a line of characters.
     |      Note that if the string is longer than a line, then in-place
     |      updating may not work (it will print a new line at each refresh).
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from tqdm._tqdm.tqdm:
     |  
     |  monitor = None
     |  
     |  monitor_interval = 10
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from tqdm._utils.Comparable:
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __ge__(self, other)
     |      Return self>=value.
     |  
     |  __gt__(self, other)
     |      Return self>value.
     |  
     |  __le__(self, other)
     |      Return self<=value.
     |  
     |  __lt__(self, other)
     |      Return self<value.
     |  
     |  __ne__(self, other)
     |      Return self!=value.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from tqdm._utils.Comparable:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    s2i_client(filename, put_file=True, get_file=True, cleanup_raw=True, cleanup_processed=True, remote_dir='/tmp', host=None, port=22, username=None, ssh_key=None, password=None, debug_level=20)
        Runs siemens_to_ismrmrd on a remote computer.
        
        Main idea: allow users to use siemens_to_ismrmrd even if they don't have
        it installed locally.  They will, however, require SSH access to computer
        that does have it installed.
        
        Client puts file on server using SFTP, runs siemens_to_ismrmrd over SSH,
        and gets the file back using SFTP.  Username, password, hostname, and port
        is retrieved from the active profile in profiles.config.  Default port is
        22.  If no password is found, the RSA SSH key will be used from either the
        specified directory in profiles.config or, if empty, use '~/.ssh/id_rsa'.
        
        filename -- Raw data (.dat) file on the local machine (if put_file is True)
                    or on the remote machine (if put_file is False).
        put_file -- Whether or not to copy the raw data file from local to remote.
        get_file -- Whether or not to copy the processed file from machine to local.
        cleanup_raw -- Whether or not to delete raw data on remote.
        cleanup_processed -- Whether or not to delete processed data on remote.
        remote_dir -- Working directory on remote (default in /tmp).
        host -- hostname of remote machine.
        port -- Port of remote machine to connect to.
        username -- Username to use for SSH/SFTP connections.
        ssh_key -- RSA private key file to use for SSH/SFTP connections.
        password -- Password to use fr SSH/SFTP connections (stored in plaintext).
        debug_level -- Level of verbosity; see python logging module.


```


## mr_utils.load_data.xprot

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/xprot.py)

```
NAME
    mr_utils.load_data.xprot

CLASSES
    builtins.object
        XProtLex
        XProtParser
    
    class XProtLex(builtins.object)
     |  Methods defined here:
     |  
     |  t_COMMENT(t)
     |      \#.*
     |  
     |  t_LEFTHAND(t)
     |      [a-zA-Z\[\]0-9\. _]+=
     |  
     |  t_error(t)
     |      # Error handling rule
     |  
     |  t_newline(t)
     |      \n+
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  lexer = <ply.lex.Lexer object>
     |  
     |  t_CLASS = 'Class'
     |  
     |  t_COM = 'Comment'
     |  
     |  t_CONN = 'Connection'
     |  
     |  t_CONTEXT = 'Context'
     |  
     |  t_CONTROL = 'Control'
     |  
     |  t_DEFAULT = 'Default'
     |  
     |  t_DEPEND = 'Dependency'
     |  
     |  t_DICOM = 'Dicom'
     |  
     |  t_DLL = 'Dll'
     |  
     |  t_EVASTRTAB = 'EVAStringTable'
     |  
     |  t_EVENT = 'Event'
     |  
     |  t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
     |  
     |  t_HEX = r'0x[\dabcdef]+'
     |  
     |  t_ID = 'ID'
     |  
     |  t_INFILE = 'InFile'
     |  
     |  t_INTEGER = r'-?\d+'
     |  
     |  t_LABEL = 'Label'
     |  
     |  t_LANGLE = '<'
     |  
     |  t_LBRACE = '{'
     |  
     |  t_LIMIT = 'Limit'
     |  
     |  t_LIMRANGE = 'LimitRange'
     |  
     |  t_LINE = 'Line'
     |  
     |  t_MAXSIZE = 'MaxSize'
     |  
     |  t_MEAS = 'Meas'
     |  
     |  t_MEASYAPS = 'MeasYaps'
     |  
     |  t_METHOD = 'Method'
     |  
     |  t_MINSIZE = 'MinSize'
     |  
     |  t_NAME = 'Name'
     |  
     |  t_PARAM = 'Param'
     |  
     |  t_PARRAY = 'ParamArray'
     |  
     |  t_PBOOL = 'ParamBool'
     |  
     |  t_PCARDLAYOUT = 'ParamCardLayout'
     |  
     |  t_PCHOICE = 'ParamChoice'
     |  
     |  t_PDBL = 'ParamDouble'
     |  
     |  t_PERIOD = r'\.'
     |  
     |  t_PFUNCT = 'ParamFunctor'
     |  
     |  t_PHOENIX = 'Phoenix'
     |  
     |  t_PIPE = 'Pipe'
     |  
     |  t_PIPESERVICE = 'PipeService'
     |  
     |  t_PLNG = 'ParamLong'
     |  
     |  t_PMAP = 'ParamMap'
     |  
     |  t_POS = 'Pos'
     |  
     |  t_PRECISION = 'Precision'
     |  
     |  t_PROTCOMP = 'ProtocolComposer'
     |  
     |  t_PSTR = 'ParamString'
     |  
     |  t_RANGLE = '>'
     |  
     |  t_RBRACE = '}'
     |  
     |  t_REPR = 'Repr'
     |  
     |  t_SCINOT = r'([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))'
     |  
     |  t_SPICE = 'Spice'
     |  
     |  t_STRING = r'\"(.|\n)*?\"'
     |  
     |  t_TOOLTIP = 'Tooltip'
     |  
     |  t_UNIT = 'Unit'
     |  
     |  t_USERVERSION = 'Userversion'
     |  
     |  t_VISIBLE = 'Visible'
     |  
     |  t_XPROT = 'XProtocol'
     |  
     |  t_ignore = ' \t'
     |  
     |  tokens = ('RANGLE', 'LANGLE', 'PERIOD', 'RBRACE', 'LBRACE', 'STRING', ...
    
    class XProtParser(builtins.object)
     |  Methods defined here:
     |  
     |  raw2xml(self, xprot)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  brace_state = []
     |  
     |  mod = ''
     |  
     |  name = ''
     |  
     |  node_label = ''
     |  
     |  xml = ''


```


## mr_utils.load_data.xprot_parser

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/xprot_parser.py)

```
NAME
    mr_utils.load_data.xprot_parser

CLASSES
    builtins.object
        XProtLexer
        XProtParser
    
    class XProtLexer(builtins.object)
     |  Methods defined here:
     |  
     |  t_COMMENT(t)
     |      \#.*
     |  
     |  t_error(t)
     |      # Error handling rule
     |  
     |  t_newline(t)
     |      \n+
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  lexer = <ply.lex.Lexer object>
     |  
     |  t_CLASS = 'Class'
     |  
     |  t_COMMENTTAG = 'Comment'
     |  
     |  t_CONNECTION = 'Connection'
     |  
     |  t_CONTEXT = 'Context'
     |  
     |  t_CONTROL = 'Control'
     |  
     |  t_DEFAULT = 'Default'
     |  
     |  t_DEPENDENCY = 'Dependency'
     |  
     |  t_DLL = 'Dll'
     |  
     |  t_EVASTRTAB = 'EVAStringTable'
     |  
     |  t_EVENT = 'Event'
     |  
     |  t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
     |  
     |  t_ID = 'ID'
     |  
     |  t_INFILE = 'InFile'
     |  
     |  t_INTEGER = r'-?\d+'
     |  
     |  t_LABEL = 'Label'
     |  
     |  t_LANGLE = '<'
     |  
     |  t_LBRACE = '{'
     |  
     |  t_LIMIT = 'Limit'
     |  
     |  t_LIMITRANGE = 'LimitRange'
     |  
     |  t_MAXSIZE = 'MaxSize'
     |  
     |  t_METHOD = 'Method'
     |  
     |  t_MINSIZE = 'MinSize'
     |  
     |  t_NAME = 'Name'
     |  
     |  t_PARAM = 'Param'
     |  
     |  t_PARAMARRAY = 'ParamArray'
     |  
     |  t_PARAMBOOL = 'ParamBool'
     |  
     |  t_PARAMCARDLAYOUT = 'ParamCardLayout'
     |  
     |  t_PARAMCHOICE = 'ParamChoice'
     |  
     |  t_PARAMDOUBLE = 'ParamDouble'
     |  
     |  t_PARAMFUNCTOR = 'ParamFunctor'
     |  
     |  t_PARAMLONG = 'ParamLong'
     |  
     |  t_PARAMMAP = 'ParamMap'
     |  
     |  t_PARAMSTRING = 'ParamString'
     |  
     |  t_PERIOD = r'\.'
     |  
     |  t_PIPE = 'Pipe'
     |  
     |  t_PIPESERVICE = 'PipeService'
     |  
     |  t_POS = 'Pos'
     |  
     |  t_PRECISION = 'Precision'
     |  
     |  t_PROTOCOLCOMPOSER = 'ProtocolComposer'
     |  
     |  t_QUOTED_STRING = r'\"(.|\n)*?\"'
     |  
     |  t_RANGLE = '>'
     |  
     |  t_RBRACE = '}'
     |  
     |  t_REPR = 'Repr'
     |  
     |  t_TOOLTIP = 'Tooltip'
     |  
     |  t_UNIT = 'Unit'
     |  
     |  t_USERVERSION = 'Userversion'
     |  
     |  t_VISIBLE = 'Visible'
     |  
     |  t_XPROT = 'XProtocol'
     |  
     |  t_ignore = ' \t'
     |  
     |  tokens = ('RANGLE', 'LANGLE', 'LBRACE', 'RBRACE', 'PERIOD', 'XPROT', '...
    
    class XProtParser(builtins.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  parse(self, xprot)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    reduce(...)
        reduce(function, sequence[, initial]) -> value
        
        Apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
        ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
        of the sequence in the calculation, and serves as a default when the
        sequence is empty.


```

