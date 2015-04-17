/**
 * Reading device state from the house app.
 */
using System;

namespace api
{
/**
 * Class which reads state from the house app.
 */
public class HouseInput : IDeviceInput
{
	public HouseInput()
	{
	}

	public bool read(Device dev)
	{
		return true;
	}
}
}

