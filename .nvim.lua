local make = function()
	local Job = require("plenary.job")
	Job:new({
		command = "bash",
		args = { "-c", "make" },
		on_exit = function(job, return_val)
			print(vim.inspect(job:result()))
		end,
	}):start()
end

return vim.api.nvim_create_autocmd({ "BufWritePost" }, {
	pattern = "*",
	callback = function(event)
		make()
	end,
})
