-- Temporary Studio test helper; never parent this into a production build.
local RunService = game:GetService("RunService")
local GuiService = game:GetService("GuiService")
local UserInputService = game:GetService("UserInputService")
local Input = {}
Input.__index = Input

function Input.new()
	assert(RunService:IsStudio() and RunService:IsClient(), "Virtual input fixtures require a Studio client")
	return setmetatable({ device = UserInputService:CreateVirtualInput(), held = {} }, Input)
end

function Input:click(button)
	assert(button:IsA("GuiButton") and button.Visible, "Expected a visible game button")
	local ancestor = button.Parent
	while ancestor do
		if ancestor:IsA("GuiObject") then
			assert(ancestor.Visible, "Button is inside hidden UI")
		end
		if ancestor:IsA("ScreenGui") then
			assert(ancestor.Enabled, "Button screen is disabled")
		end
		ancestor = ancestor.Parent
	end
	-- AbsolutePosition is in the core UI coordinate space; account for device notches too.
	local point = button.AbsolutePosition
		+ button.AbsoluteSize / 2
		- GuiService:GetInsetArea(Enum.ScreenInsets.None).Min
	self.device:SendMousePosition(point)
	task.wait(0.08)
	self.device:SendMouseButton(point, Enum.UserInputType.MouseButton1, true, 0)
	task.wait(0.08)
	self.device:SendMouseButton(point, Enum.UserInputType.MouseButton1, false, 0)
end

function Input:key(keyCode, seconds)
	self.held[keyCode] = true
	self.device:SendKey(true, keyCode, false)
	task.wait(seconds or 0.08)
	self.device:SendKey(false, keyCode, false)
	self.held[keyCode] = nil
end

function Input:release()
	for keyCode in self.held do
		pcall(function()
			self.device:SendKey(false, keyCode, false)
		end)
	end
	table.clear(self.held)
end

function Input:waitUntil(predicate, seconds, description)
	local deadline = os.clock() + seconds
	repeat
		if predicate() then
			return
		end
		task.wait(0.05)
	until os.clock() >= deadline
	error("Timed out: " .. description, 2)
end

return Input
