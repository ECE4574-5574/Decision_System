/**
 * Input for writing device state to the Server API
 */
using System;

namespace api
{
public class ServerOutput : IDeviceOutput
{
	public ServerOutput()
	{
	}

	public bool write(Device dev)
	{
		return true;
	}
}
}

