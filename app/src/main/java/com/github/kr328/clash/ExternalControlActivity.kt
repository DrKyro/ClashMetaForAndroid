package com.github.kr328.clash

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import com.github.kr328.clash.common.constants.Intents
import com.github.kr328.clash.common.util.intent
import com.github.kr328.clash.common.util.setUUID
import com.github.kr328.clash.design.MainDesign
import com.github.kr328.clash.design.ui.ToastDuration
import com.github.kr328.clash.remote.Remote
import com.github.kr328.clash.remote.StatusClient
import com.github.kr328.clash.service.model.Profile
import com.github.kr328.clash.service.remote.IProfileManager
import com.github.kr328.clash.util.startClashService
import com.github.kr328.clash.util.stopClashService
import com.github.kr328.clash.util.withProfile
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.launch
import java.io.File
import java.util.*
import com.github.kr328.clash.design.R

class ExternalControlActivity : Activity(), CoroutineScope by MainScope() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        when(intent.action) {
            Intent.ACTION_VIEW -> {
                val uri = intent.data ?: return finish()
                val url = uri.getQueryParameter("url") ?: return finish()

                launch {
                    withProfile {
                        val type = when (uri.getQueryParameter("type")?.lowercase(Locale.getDefault())) {
                            "url" -> Profile.Type.Url
                            "file" -> Profile.Type.File
                            else -> Profile.Type.Url
                        }
                        val name = uri.getQueryParameter("name") ?: getString(R.string.new_profile)

                        val uuid = create(type, name, url)
                        patch(uuid, name, url, 0)
                        startActivity(PropertiesActivity::class.intent.setUUID(uuid))
                        finish()
                    }
                }
            }

            Intents.ACTION_TOGGLE_CLASH -> if(Remote.broadcasts.clashRunning) {
                stopClash()
            }
            else {
                startClash()
            }

            Intents.ACTION_START_CLASH -> if(!Remote.broadcasts.clashRunning) {
                startClash()
            }
            else {
                Toast.makeText(this, R.string.external_control_started, Toast.LENGTH_LONG).show()
            }

            Intents.ACTION_STOP_CLASH -> if(Remote.broadcasts.clashRunning) {
                stopClash()
            }
            else {
                Toast.makeText(this, R.string.external_control_stopped, Toast.LENGTH_LONG).show()
            }

            Intents.ACTION_SWITCH_TO_CONFIG -> {
                val configPath = intent.getStringExtra(Intents.EXTRA_CONFIG_PATH)
                if (configPath != null) {
                    switchToConfig(configPath)
                } else {
                    Toast.makeText(this, "配置文件路径不能为空", Toast.LENGTH_LONG).show()
                }
            }

            Intents.ACTION_SWITCH_TO_URL -> {
                val configUrl = intent.getStringExtra(Intents.EXTRA_CONFIG_URL)
                if (configUrl != null) {
                    switchToUrl(configUrl)
                } else {
                    Toast.makeText(this, "配置文件URL不能为空", Toast.LENGTH_LONG).show()
                }
            }
        }
        return finish()
    }

    private fun startClash() {
//        if (currentProfile == null) {
//            Toast.makeText(this, R.string.no_profile_selected, Toast.LENGTH_LONG).show()
//            return
//        }
        val vpnRequest = startClashService()
        if (vpnRequest != null) {
            Toast.makeText(this, R.string.unable_to_start_vpn, Toast.LENGTH_LONG).show()
            return
        }
        Toast.makeText(this, R.string.external_control_started, Toast.LENGTH_LONG).show()
    }

    private fun stopClash() {
        stopClashService()
        Toast.makeText(this, R.string.external_control_stopped, Toast.LENGTH_LONG).show()
    }

    private fun switchToConfig(configPath: String) {
        val configFile = File(configPath)
        if (!configFile.exists()) {
            Toast.makeText(this, "配置文件不存在: $configPath", Toast.LENGTH_LONG).show()
            return
        }

        launch {
            try {
                withProfile {
                    val fileName = File(configPath).nameWithoutExtension
                    // 直接使用文件路径，不加file://协议前缀
                    val uuid = create(Profile.Type.File, fileName, configPath)
                    patch(uuid, fileName, configPath, 0)
                    
                    // 提交配置文件并等待完成
                    commit(uuid, null)
                    
                    // 再次查询配置文件以确保提交成功
                    val profile = queryByUUID(uuid)
                    if (profile != null) {
                        // 设置为活动配置
                        setActive(profile)
                        runOnUiThread {
                            Toast.makeText(this@ExternalControlActivity, "已切换到配置文件: $configPath", Toast.LENGTH_LONG).show()
                        }
                    } else {
                        runOnUiThread {
                            Toast.makeText(this@ExternalControlActivity, "切换配置失败: 无法找到创建的配置", Toast.LENGTH_LONG).show()
                        }
                    }
                }
            } catch (e: Exception) {
                Log.e("ExternalControlActivity", "切换配置失败", e)
                runOnUiThread {
                    Toast.makeText(this@ExternalControlActivity, "切换配置失败: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    private fun switchToUrl(configUrl: String) {
        launch {
            try {
                withProfile {
                    val fileName = "URL配置_${System.currentTimeMillis()}"
                    val uuid = create(Profile.Type.Url, fileName, configUrl)
                    patch(uuid, fileName, configUrl, 0)
                    commit(uuid, null)
                    setActive(queryByUUID(uuid)!!)
                    
                    runOnUiThread {
                        Toast.makeText(this@ExternalControlActivity, "已切换到URL配置: $configUrl", Toast.LENGTH_LONG).show()
                    }
                }
            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this@ExternalControlActivity, "切换配置失败: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
        finish()
    }
}