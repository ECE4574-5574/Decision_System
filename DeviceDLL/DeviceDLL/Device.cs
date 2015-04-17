/**
 * Base class for all devices in the HATS system.
 * \author Jason Ziglar <jpz@vt.edu>
 */
using System;

namespace api
{
/**
 * Base class representing the common parameters for any given device. All Devices inherit from this
 */
public abstract class Device
{
	public Device(IDeviceInput inp, IDeviceOutput outp)
	{
		_in = inp;
		_out = outp;
        LastUpdate = DateTime.Now.ToUniversalTime();
	}

	public FullID ID
	{
		get;
		set;
	}

    public DateTime LastUpdate
    {
        get;
        set;
    }

	/**
	 * User friendly name for this device.
	 */
	public string Name
	{
		get;
		set;
	}

	protected IDeviceInput _in;
	protected IDeviceOutput _out;
}
}

