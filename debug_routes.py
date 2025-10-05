from app import create_app

app = create_app()

def debug_blueprints():
    with app.app_context():
        print("=== 应用路由详情 ===")
        
        # 按蓝图分组显示路由
        blueprints = {}
        for rule in app.url_map.iter_rules():
            if 'static' in rule.endpoint:
                continue
                
            # 提取蓝图名称
            if '.' in rule.endpoint:
                bp_name = rule.endpoint.split('.')[0]
            else:
                bp_name = 'main'
                
            if bp_name not in blueprints:
                blueprints[bp_name] = []
                
            blueprints[bp_name].append({
                'endpoint': rule.endpoint,
                'rule': rule.rule,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
            })
        
        for bp_name, routes in blueprints.items():
            print(f"\n--- {bp_name.upper()} 蓝图 ---")
            for route in sorted(routes, key=lambda x: x['rule']):
                print(f"  {route['endpoint']:25} {route['rule']:35} {route['methods']}")

if __name__ == '__main__':
    debug_blueprints()