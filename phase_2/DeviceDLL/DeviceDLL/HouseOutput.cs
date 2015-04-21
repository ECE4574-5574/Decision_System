/**
 * Writing device state to the house app.
 */
using System;

namespace api
{

/**
 * Class for writing device state to the house.
 */
public class HouseOutput : IDeviceOutput
{
	public HouseOutput()
	{
	}

	public bool write(Device dev)
	{
		//TODO: Implement writing to the house
		return true;
	}
}

}
